"""Marcacao da faixa de dominio: limpeza geodesica dos sinistros.

Mede a distancia de cada sinistro ao eixo da sua BR, com a geometria oficial do
SNV em resolucao cheia, e grava uma marca no banco: dentro ou fora de uma faixa
de dominio de 50 metros para cada lado. O mapa usa a marca para desenhar apenas
os sinistros de dentro. O custo e a contagem por segmento nao mudam, porque o
acidente e real e a ancoragem usa o quilometro, e nao a coordenada.

A distancia se mede contra a geometria cheia do shapefile, e nao contra a versao
simplificada do banco, que se afasta do eixo em ate 90 metros e inverteria o teste.

Uso:
    python scripts/marcar_faixa_dominio.py \
        --shp "D:/PPgTI_UFRN/DNIT/SNV/GIS (SHP e KLM)/SNV_202507A.shp" \
        --uf RN --faixa 50 --banco dados/consolidado.db

Spec em openspec/changes/2026-09-09-faixa-de-dominio/.
"""
from __future__ import annotations

import argparse
import math
import sqlite3
from collections import defaultdict
from pathlib import Path

FAIXA_PADRAO_M = 50.0
METROS_POR_GRAU = 111_320.0


def _projecao(lat0: float):
    """Devolve uma funcao que projeta (lat, lng) em metros, equiretangular.

    A longitude e corrigida pelo cosseno da latitude de referencia. Para a
    extensao de um estado, o erro e desprezivel diante do limiar de metros.
    """
    kx = METROS_POR_GRAU * math.cos(math.radians(lat0))
    ky = METROS_POR_GRAU
    return lambda lat, lng: (lng * kx, lat * ky)


def _geometria_da_malha(shp: str | Path, uf: str, projeta):
    """Le o shapefile e devolve a geometria da UF, por BR e como malha inteira.

    A geometria por BR mede o sinistro contra a sua propria rodovia. A malha
    inteira, uniao de todas as BRs, mede o sinistro sem BR ou sem ancoragem, que
    de outro modo ficaria sem avaliacao.
    """
    import shapefile
    from shapely.geometry import LineString, MultiLineString
    from shapely.ops import unary_union

    leitor = shapefile.Reader(str(shp))
    campos = [f[0] for f in leitor.fields[1:]]
    i_br, i_uf = campos.index("vl_br"), campos.index("sg_uf")
    linhas: dict[int, list] = defaultdict(list)
    todas: list = []
    for registro in leitor.iterShapeRecords():
        rec = registro.record
        if rec[i_uf] != uf:
            continue
        pontos = registro.shape.points
        if len(pontos) < 2:
            continue
        linha = LineString([projeta(y, x) for x, y in pontos])
        todas.append(linha)
        try:
            linhas[int(rec[i_br])].append(linha)
        except (TypeError, ValueError):
            pass
    geo_br = {br: MultiLineString(ls) for br, ls in linhas.items()}
    return geo_br, unary_union(todas)


def _criar_tabela(con: sqlite3.Connection) -> None:
    con.execute(
        "CREATE TABLE IF NOT EXISTS qualidade_geo ("
        " id TEXT PRIMARY KEY, br INTEGER, distancia_m REAL, dentro_faixa INTEGER)"
    )


def marcar_faixa(shp: str | Path, uf: str, con: sqlite3.Connection, *,
                 faixa_m: float = FAIXA_PADRAO_M, lat0: float = -5.8) -> dict:
    """Marca cada sinistro como dentro ou fora da faixa de dominio da sua BR.

    Returns:
        Resumo com o total medido, quantos ficaram fora e a distancia maxima.
    """
    from shapely.geometry import Point

    uf = uf.upper()
    projeta = _projecao(lat0)
    geo_br, geo_malha = _geometria_da_malha(shp, uf, projeta)
    _criar_tabela(con)

    # todas as ocorrencias com coordenada, ancoradas ou nao: o sinistro sem BR
    # ou sem ancoragem tambem e um erro de coordenada a limpar, medido contra a
    # malha inteira
    consulta = (
        "SELECT o.id, o.br, o.latitude, o.longitude "
        "  FROM ocorrencias o "
        " WHERE o.uf = ? "
        "   AND o.latitude IS NOT NULL AND o.longitude IS NOT NULL"
    )
    total = fora = sem_br = 0
    dist_max = 0.0
    registros = []
    for _id, br, lat, lng in con.execute(consulta, (uf,)):
        geo = geo_br.get(br)
        if geo is None:
            geo = geo_malha
            sem_br += 1
        d = geo.distance(Point(projeta(lat, lng)))
        dentro = 1 if d <= faixa_m else 0
        fora += 1 - dentro
        dist_max = max(dist_max, d)
        total += 1
        registros.append((_id, br, d, dentro))

    con.executemany(
        "INSERT OR REPLACE INTO qualidade_geo (id, br, distancia_m, dentro_faixa)"
        " VALUES (?, ?, ?, ?)",
        registros,
    )
    con.commit()
    return {"total": total, "fora": fora, "sem_br": sem_br,
            "distancia_maxima_m": round(dist_max, 1), "faixa_m": faixa_m}


def main() -> None:
    p = argparse.ArgumentParser(description="Marca a faixa de dominio dos sinistros.")
    p.add_argument("--shp", required=True, help="caminho do shapefile do SNV")
    p.add_argument("--uf", required=True, help="unidade da federacao, ex.: RN")
    p.add_argument("--banco", required=True, help="caminho do banco consolidado")
    p.add_argument("--faixa", type=float, default=FAIXA_PADRAO_M,
                   help="meia largura da faixa em metros (padrao 50)")
    p.add_argument("--lat0", type=float, default=-5.8,
                   help="latitude de referencia da projecao")
    args = p.parse_args()

    con = sqlite3.connect(args.banco)
    try:
        r = marcar_faixa(args.shp, args.uf, con, faixa_m=args.faixa, lat0=args.lat0)
    finally:
        con.close()
    print(f"marcados {r['total']} sinistros de {args.uf}, faixa {r['faixa_m']:.0f} m")
    print(f"  fora da faixa: {r['fora']} ({100*r['fora']/max(r['total'],1):.1f}%)")
    print(f"  sem BR, medidos contra a malha inteira: {r['sem_br']}")
    print(f"  distancia maxima: {r['distancia_maxima_m']:,.1f} m")


if __name__ == "__main__":
    main()
