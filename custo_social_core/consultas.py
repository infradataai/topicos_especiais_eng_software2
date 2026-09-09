"""Consultas somente leitura do esquema de sinistros, para a camada de aplicacao.

A camada web recebe uma sqlite3.Connection e nao deve escrever SQL do esquema do
nucleo. Este modulo concentra esse SQL e devolve listas de dicionarios. Usa
sqlite3 da biblioteca padrao, e nao o SQLAlchemy do persistencia.py, para que a
fronteira de aplicacao nao carregue o mapeador.

Spec em openspec/changes/2026-09-09-mapa-trechos-criticos/specs/consulta/.
"""
from __future__ import annotations

import sqlite3

# Tabelas sem as quais nenhuma consulta deste modulo faz sentido.
TABELAS_NUCLEO = ("ocorrencias", "custo_ocorrencia", "segmentos_snv", "ancoragem")

# Colunas pelas quais o cliente pode ordenar. Fora desta lista, a consulta recusa.
# A lista existe porque o nome da coluna entra na clausula ORDER BY por
# interpolacao, que o SQLite nao parametriza.
ORDENACOES_SEGMENTO = frozenset({
    "codigo", "br", "extensao", "custo_social", "ocorrencias",
    "vmda", "custo_por_km", "custo_por_veiculo_km",
})
ORDENACOES_OCORRENCIA = frozenset({"id", "br", "km", "ano", "custo_social"})

DIAS_DO_ANO = 365


def tem_esquema_de_sinistros(con: sqlite3.Connection) -> bool:
    """Diz se o banco tem as tabelas do nucleo.

    A verificacao le sqlite_master, e nao tenta uma consulta de sondagem, para
    que a ausencia das tabelas nao apareca como erro do banco.
    """
    presentes = {
        linha[0]
        for linha in con.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    }
    return all(t in presentes for t in TABELAS_NUCLEO)


def _direcao(direcao: str) -> str:
    if direcao.lower() not in {"asc", "desc"}:
        raise ValueError("direcao deve ser asc ou desc")
    return direcao.upper()


_SQL_SEGMENTOS = f"""
WITH anc AS (
    SELECT a.id, a.codigo_segmento AS codigo, a.safra
      FROM ancoragem a
      JOIN ocorrencias o ON o.id = a.id
     WHERE o.uf = :uf AND a.codigo_segmento IS NOT NULL
),
-- a extensao vem da safra mais recente: somar todas as safras contaria a mesma
-- extensao fisica varias vezes e inflaria a malha do estado
recente AS (
    SELECT codigo, MAX(safra) AS safra FROM anc GROUP BY codigo
),
exp AS (
    SELECT codigo, vmda, n_postos
      FROM exposicao_segmento e
     WHERE e.ano = (SELECT MAX(ano) FROM exposicao_segmento WHERE codigo = e.codigo)
)
SELECT s.codigo, s.br, s.uf, s.extensao, s.regime, s.jurisdicao,
       SUM(c.total)    AS custo_social,
       COUNT(*)        AS ocorrencias,
       MAX(e.vmda)     AS vmda,
       MAX(e.n_postos) AS n_postos,
       CASE WHEN s.extensao > 0
            THEN SUM(c.total) / s.extensao END AS custo_por_km,
       CASE WHEN MAX(e.vmda) > 0 AND s.extensao > 0
            THEN SUM(c.total) / (MAX(e.vmda) * s.extensao * {DIAS_DO_ANO})
            END AS custo_por_veiculo_km
  FROM anc
  JOIN custo_ocorrencia c ON c.id = anc.id
  JOIN recente          r ON r.codigo = anc.codigo
  JOIN segmentos_snv    s ON s.codigo = r.codigo AND s.safra = r.safra
LEFT JOIN exp           e ON e.codigo = s.codigo
 GROUP BY s.codigo, s.br, s.uf, s.extensao, s.regime, s.jurisdicao
"""


def _dicionarios(cursor: sqlite3.Cursor) -> list[dict]:
    nomes = [c[0] for c in cursor.description or []]
    return [dict(zip(nomes, linha)) for linha in cursor.fetchall()]


def segmentos_criticos(con: sqlite3.Connection, uf: str, *,
                       ordenar_por: str = "custo_por_km", direcao: str = "desc",
                       limite: int = 100, deslocamento: int = 0) -> list[dict]:
    """Uma linha por segmento, com as duas leituras de criticidade.

    O custo por quilometro divide o custo pela extensao. O custo por
    veiculo-quilometro divide o mesmo custo pela exposicao anual. O segmento sem
    volume medido recebe nulo na segunda leitura e permanece na primeira.

    Raises:
        ValueError: se a coluna de ordenacao nao estiver na lista permitida.
    """
    if ordenar_por not in ORDENACOES_SEGMENTO:
        raise ValueError(f"ordenacao nao permitida: {ordenar_por}")
    sql = (f"{_SQL_SEGMENTOS} ORDER BY {ordenar_por} {_direcao(direcao)} "
           f"LIMIT :limite OFFSET :deslocamento")
    cursor = con.execute(sql, {"uf": uf, "limite": limite, "deslocamento": deslocamento})
    return _dicionarios(cursor)


def contar_segmentos(con: sqlite3.Connection, uf: str) -> int:
    """Quantos segmentos da unidade da federacao tem ocorrencia ancorada."""
    sql = f"SELECT COUNT(*) FROM ({_SQL_SEGMENTOS})"
    return con.execute(sql, {"uf": uf}).fetchone()[0]


def _filtros_ocorrencia(uf: str, br: int | None, ano: int | None):
    clausulas = ["o.uf = :uf"]
    valores: dict = {"uf": uf}
    if br is not None:
        clausulas.append("o.br = :br")
        valores["br"] = br
    if ano is not None:
        clausulas.append("o.ano = :ano")
        valores["ano"] = ano
    return " AND ".join(clausulas), valores


def ocorrencias(con: sqlite3.Connection, uf: str, *, br: int | None = None,
                ano: int | None = None, ordenar_por: str = "id",
                direcao: str = "asc", limite: int = 100,
                deslocamento: int = 0) -> list[dict]:
    """Ocorrencias com coordenada, categoria e custo, para alimentar o mapa."""
    if ordenar_por not in ORDENACOES_OCORRENCIA:
        raise ValueError(f"ordenacao nao permitida: {ordenar_por}")
    where, valores = _filtros_ocorrencia(uf, br, ano)
    coluna = "c.total" if ordenar_por == "custo_social" else f"o.{ordenar_por}"
    valores.update({"limite": limite, "deslocamento": deslocamento})
    cursor = con.execute(
        "SELECT o.id, o.uf, o.br, o.km, o.ano, o.data, o.classificacao_acidente, "
        "       o.latitude, o.longitude, c.total AS custo_social, c.categoria, "
        "       a.codigo_segmento AS segmento "
        "  FROM ocorrencias o "
        "  LEFT JOIN custo_ocorrencia c ON c.id = o.id "
        "  LEFT JOIN ancoragem       a ON a.id = o.id "
        f" WHERE {where} "
        f" ORDER BY {coluna} {_direcao(direcao)} LIMIT :limite OFFSET :deslocamento",
        valores,
    )
    return _dicionarios(cursor)


def contar_ocorrencias(con: sqlite3.Connection, uf: str, *, br: int | None = None,
                       ano: int | None = None) -> int:
    """Quantas ocorrencias atendem ao filtro, para a paginacao."""
    where, valores = _filtros_ocorrencia(uf, br, ano)
    return con.execute(f"SELECT COUNT(*) FROM ocorrencias o WHERE {where}", valores).fetchone()[0]


def resumo(con: sqlite3.Connection, uf: str) -> dict:
    """Totais da unidade da federacao, para o cabecalho da pagina."""
    linha = con.execute(
        "SELECT COUNT(*) AS ocorrencias, "
        "       COALESCE(SUM(c.total), 0) AS custo_social, "
        "       MIN(o.ano) AS ano_inicial, MAX(o.ano) AS ano_final "
        "  FROM ocorrencias o LEFT JOIN custo_ocorrencia c ON c.id = o.id "
        " WHERE o.uf = :uf",
        {"uf": uf},
    )
    dados = _dicionarios(linha)[0]
    dados["segmentos"] = contar_segmentos(con, uf)
    return dados
