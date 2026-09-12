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
        " desenhar INTEGER, PRIMARY KEY (safra, codigo))"
    )


def _segmentos_do_banco(con: sqlite3.Connection, uf: str) -> dict:
    """Codigo -> (br, km_inicial, km_final) dos segmentos ancorados da UF.

    Serve para preencher, por sobreposicao de km, o tracado dos codigos que o
    shapefile nao traz sob o mesmo codigo, por recodificacao entre safras.
    """
    if not con.execute("SELECT 1 FROM sqlite_master WHERE type='table' "
                       "AND name='segmentos_snv'").fetchone():
        return {}
    cursor = con.execute(
        "SELECT s.codigo, s.br, MIN(s.km_inicial), MAX(s.km_final) "
        "  FROM segmentos_snv s "
        "  JOIN ancoragem a ON a.codigo_segmento = s.codigo "
        "  JOIN ocorrencias o ON o.id = a.id "
        " WHERE o.uf = :uf GROUP BY s.codigo, s.br",
        {"uf": uf},
    )
    return {cod: (br, ki, kf) for cod, br, ki, kf in cursor}


def ingerir_geometria(shp: str | Path, uf: str, safra: str,
                      con: sqlite3.Connection, *,
                      tolerancia: float = TOLERANCIA_PADRAO) -> int:
    """Le o shapefile, filtra a UF e grava o tracado simplificado de cada trecho.

    A leitura usa o codigo do trecho (`vl_codigo`), identico ao codigo do nosso
    banco. Os codigos que o shapefile nao traz, por recodificacao entre safras,
    sao preenchidos pela uniao dos trechos da mesma BR que cobrem a faixa de km
    do segmento, na ordem do km.

    Returns:
        Quantos segmentos foram gravados.
    """
    import shapefile

    leitor = shapefile.Reader(str(shp))
    campos = [f[0] for f in leitor.fields[1:]]
    i_cod = campos.index("vl_codigo")
    i_uf = campos.index("sg_uf")
    i_br = campos.index("vl_br")
    # os campos de km sustentam o preenchimento por sobreposicao; sem eles, so o
    # casamento por codigo ocorre
    i_ki = campos.index("vl_km_inic") if "vl_km_inic" in campos else None
    i_kf = campos.index("vl_km_fina") if "vl_km_fina" in campos else None

    _criar_tabela(con)
    uf = uf.upper()
    por_codigo: dict[str, tuple] = {}       # codigo -> (br, pontos)
    por_br: dict[int, list] = {}            # br -> [(km_ini, km_fim, pontos)]
    for registro in leitor.iterShapeRecords():
        rec = registro.record
        if rec[i_uf] != uf:
            continue
        pontos = list(registro.shape.points)
        try:
            br = int(rec[i_br])
        except (TypeError, ValueError):
            br = None
        por_codigo.setdefault(rec[i_cod], (br, pontos))
        if br is not None and i_ki is not None and i_kf is not None:
            por_br.setdefault(br, []).append((rec[i_ki], rec[i_kf], pontos))

    def grava(codigo, br, pontos_brutos, desenhar):
        con.execute(
            "INSERT OR REPLACE INTO geometria_segmento"
            " (safra, codigo, br, uf, pontos, desenhar) VALUES (?, ?, ?, ?, ?, ?)",
            (safra, codigo, br, uf, json.dumps(simplificar(pontos_brutos, tolerancia)),
             desenhar),
        )

    gravados = 0
    for cod, (br, pontos) in por_codigo.items():
        grava(cod, br, pontos, 1)
        gravados += 1

    # preenche os codigos do nosso banco ausentes no shapefile, por sobreposicao
    # de km na mesma BR, na ordem do km. Sao codigos antigos, ja desenhados pelos
    # codigos vigentes, entao entram com desenhar = 0, para nao dobrar a linha.
    for cod, (br, ki, kf) in _segmentos_do_banco(con, uf).items():
        if cod in por_codigo or br not in por_br:
            continue
        cobrem = sorted((s for s in por_br[br] if s[1] >= ki and s[0] <= kf),
                        key=lambda s: s[0])
        if not cobrem:
            continue
        pontos = [p for _, _, pts in cobrem for p in pts]
        grava(cod, br, pontos, 0)
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
