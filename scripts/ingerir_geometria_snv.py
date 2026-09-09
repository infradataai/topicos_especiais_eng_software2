"""Ingestao da base geometrica do SNV para a tabela geometria_segmento.

Le o shapefile da base geometrica do DNIT, filtra a unidade da federacao,
simplifica cada tracado por Douglas-Peucker e grava o resultado no banco
consolidado. O tracado alimenta o desenho dos trechos no mapa.

A base bruta do DNIT tem dezenas de megabytes e fica fora do controle de versao.
Apos a simplificacao, o tracado de uma unidade da federacao ocupa dezenas de
quilobytes, e viaja junto do banco.

Uso:
    python scripts/ingerir_geometria_snv.py \
        --shp "D:/PPgTI_UFRN/DNIT/SNV/GIS (SHP e KLM)/SNV_202507A.shp" \
        --uf RN --safra 202507A --banco dados/consolidado.db

Spec em openspec/changes/2026-09-09-geometria-oficial-snv/.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

# Tolerancia de simplificacao, em graus. Cerca de 90 metros, abaixo do que se
# distingue na escala do estado.
TOLERANCIA_PADRAO = 0.0008


def simplificar(pontos: list[tuple[float, float]], tolerancia: float) -> list[list[float]]:
    """Simplifica uma polilinha e devolve os pontos como [lat, lng].

    Recebe pontos no formato (lng, lat), como vem do shapefile, e devolve
    [lat, lng], como a biblioteca de mapa espera.
    """
    from shapely.geometry import LineString

    if len(pontos) < 2:
        return [[lat, lng] for lng, lat in pontos]
    linha = LineString(pontos).simplify(tolerancia, preserve_topology=False)
    return [[lat, lng] for lng, lat in linha.coords]


def _criar_tabela(con: sqlite3.Connection) -> None:
    con.execute(
        "CREATE TABLE IF NOT EXISTS geometria_segmento ("
        " safra TEXT, codigo TEXT, br INTEGER, uf TEXT, pontos TEXT,"
        " PRIMARY KEY (safra, codigo))"
    )


def ingerir_geometria(shp: str | Path, uf: str, safra: str,
                      con: sqlite3.Connection, *,
                      tolerancia: float = TOLERANCIA_PADRAO) -> int:
    """Le o shapefile, filtra a UF e grava o tracado simplificado de cada trecho.

    A leitura usa o codigo do trecho (`vl_codigo`), identico ao codigo do nosso
    banco. Repete a mesma UF e safra em cada linha, para a consulta filtrar.

    Returns:
        Quantos segmentos foram gravados.
    """
    import shapefile

    leitor = shapefile.Reader(str(shp))
    campos = [f[0] for f in leitor.fields[1:]]
    i_cod = campos.index("vl_codigo")
    i_uf = campos.index("sg_uf")
    i_br = campos.index("vl_br")

    _criar_tabela(con)
    uf = uf.upper()
    vistos: set[str] = set()
    gravados = 0
    for registro in leitor.iterShapeRecords():
        rec = registro.record
        if rec[i_uf] != uf:
            continue
        codigo = rec[i_cod]
        if codigo in vistos:
            continue
        vistos.add(codigo)
        pontos = simplificar(list(registro.shape.points), tolerancia)
        try:
            br = int(rec[i_br])
        except (TypeError, ValueError):
            br = None
        con.execute(
            "INSERT OR REPLACE INTO geometria_segmento (safra, codigo, br, uf, pontos)"
            " VALUES (?, ?, ?, ?, ?)",
            (safra, codigo, br, uf, json.dumps(pontos)),
        )
        gravados += 1
    con.commit()
    return gravados


def main() -> None:
    p = argparse.ArgumentParser(description="Ingere a geometria do SNV no banco.")
    p.add_argument("--shp", required=True, help="caminho do shapefile do SNV")
    p.add_argument("--uf", required=True, help="unidade da federacao, ex.: RN")
    p.add_argument("--safra", required=True, help="safra da base, ex.: 202507A")
    p.add_argument("--banco", required=True, help="caminho do banco consolidado")
    p.add_argument("--tolerancia", type=float, default=TOLERANCIA_PADRAO,
                   help="tolerancia de simplificacao em graus")
    args = p.parse_args()

    con = sqlite3.connect(args.banco)
    try:
        n = ingerir_geometria(args.shp, args.uf, args.safra, con,
                              tolerancia=args.tolerancia)
    finally:
        con.close()
    print(f"geometria ingerida: {n} segmentos de {args.uf}, safra {args.safra}")


if __name__ == "__main__":
    main()
