"""Consultas somente leitura do esquema de sinistros, para a camada de aplicacao.

A camada web recebe uma sqlite3.Connection e nao deve escrever SQL do esquema do
nucleo. Este modulo concentra esse SQL e devolve listas de dicionarios. Usa
sqlite3 da biblioteca padrao, e nao o SQLAlchemy do persistencia.py, para que a
fronteira de aplicacao nao carregue o mapeador.

Spec em openspec/changes/2026-09-09-mapa-trechos-criticos/specs/consulta/.
"""
from __future__ import annotations

import json
import sqlite3

# Tabelas sem as quais nenhuma consulta deste modulo faz sentido.
TABELAS_NUCLEO = ("ocorrencias", "custo_ocorrencia", "segmentos_snv", "ancoragem")

# Colunas pelas quais o cliente pode ordenar. Fora desta lista, a consulta recusa.
# A lista existe porque o nome da coluna entra na clausula ORDER BY por
# interpolacao, que o SQLite nao parametriza.
ORDENACOES_SEGMENTO = frozenset({
    "codigo", "br", "extensao", "custo_social", "ocorrencias",
    "vmda", "custo_por_km", "custo_por_veiculo_km",
    "custo_por_km_ano", "custo_por_veiculo_km_ano",
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
),
base AS (
    SELECT s.codigo, s.br, s.uf, s.km_inicial, s.km_final, s.extensao,
           s.regime, s.jurisdicao,
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
     GROUP BY s.codigo, s.br, s.uf, s.km_inicial, s.km_final, s.extensao,
              s.regime, s.jurisdicao
)
-- as colunas anuais dividem o acumulado pelo periodo observado (:n_anos),
-- que e o intervalo de anos com ocorrencia na unidade da federacao
SELECT base.*,
       custo_por_km          / :n_anos AS custo_por_km_ano,
       custo_por_veiculo_km  / :n_anos AS custo_por_veiculo_km_ano
  FROM base
"""


def _dicionarios(cursor: sqlite3.Cursor) -> list[dict]:
    nomes = [c[0] for c in cursor.description or []]
    return [dict(zip(nomes, linha)) for linha in cursor.fetchall()]


def periodo_anos(con: sqlite3.Connection, uf: str) -> int:
    """Numero de anos observados na unidade da federacao.

    E o intervalo entre o primeiro e o ultimo ano com ocorrencia, contado de
    ponta a ponta: 2019 a 2025 sao sete anos. Serve de divisor das colunas
    anuais. Quando nao ha ocorrencia, devolve 1, para nao dividir por zero.
    """
    faixa = con.execute(
        "SELECT MIN(ano), MAX(ano) FROM ocorrencias WHERE uf = :uf", {"uf": uf}
    ).fetchone()
    if not faixa or faixa[0] is None:
        return 1
    return faixa[1] - faixa[0] + 1


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
    cursor = con.execute(sql, {"uf": uf, "n_anos": periodo_anos(con, uf),
                               "limite": limite, "deslocamento": deslocamento})
    return _dicionarios(cursor)


def contar_segmentos(con: sqlite3.Connection, uf: str) -> int:
    """Quantos segmentos da unidade da federacao tem ocorrencia ancorada."""
    sql = f"SELECT COUNT(*) FROM ({_SQL_SEGMENTOS})"
    return con.execute(sql, {"uf": uf, "n_anos": periodo_anos(con, uf)}).fetchone()[0]


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


# Teto de seguranca para os pontos do mapa. Acima disso, a resposta e cortada e
# declara o corte, para o navegador nao travar com o pais inteiro.
LIMITE_PONTOS_MAPA = 20_000


def ocorrencias_geo(con: sqlite3.Connection, uf: str, *, br: int | None = None,
                    ano: int | None = None, limite: int = LIMITE_PONTOS_MAPA) -> list[dict]:
    """Todos os pontos de sinistro com coordenada, para a camada do mapa.

    Sem paginacao: a camada do mapa precisa de todos os pontos, e nao de uma
    pagina. So os campos que o marcador usa entram, para o pacote ficar leve.
    O teto evita travar o navegador quando o filtro e amplo.
    """
    where, valores = _filtros_ocorrencia(uf, br, ano)
    valores["limite"] = limite
    cursor = con.execute(
        "SELECT o.br, o.km, o.ano, o.latitude, o.longitude, "
        "       c.total AS custo_social, c.categoria, a.codigo_segmento AS segmento "
        "  FROM ocorrencias o "
        "  LEFT JOIN custo_ocorrencia c ON c.id = o.id "
        "  LEFT JOIN ancoragem       a ON a.id = o.id "
        f" WHERE {where} AND o.latitude IS NOT NULL AND o.longitude IS NOT NULL "
        " LIMIT :limite",
        valores,
    )
    return _dicionarios(cursor)


def _amostrar(pontos: list, maximo: int) -> list:
    """Reduz a lista de pontos a no maximo `maximo`, por passo uniforme.

    Preserva o primeiro e o ultimo ponto, para nao encurtar o tracado. Sem isso
    um segmento com centenas de sinistros mandaria centenas de coordenadas ao
    navegador, sem ganho visual.
    """
    if len(pontos) <= maximo:
        return pontos
    passo = (len(pontos) - 1) / (maximo - 1)
    indices = sorted({round(i * passo) for i in range(maximo)} | {len(pontos) - 1})
    return [pontos[i] for i in indices]


def _tem_tabela(con: sqlite3.Connection, nome: str) -> bool:
    """Diz se uma tabela existe, sem levantar erro quando falta."""
    return con.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = :n",
        {"n": nome},
    ).fetchone() is not None


def _geometria_oficial(con: sqlite3.Connection, uf: str) -> dict[str, list]:
    """Tracado oficial do SNV por codigo, quando a tabela de geometria existe.

    Devolve dicionario vazio quando o banco ainda nao tem a geometria ingerida,
    para que a consulta recue para a aproximacao sem falhar.
    """
    if not _tem_tabela(con, "geometria_segmento"):
        return {}
    cursor = con.execute(
        "SELECT codigo, pontos FROM geometria_segmento WHERE uf = :uf", {"uf": uf}
    )
    return {cod: json.loads(pts) for cod, pts in cursor if pts}


def _geometria_por_sinistros(con: sqlite3.Connection, uf: str,
                             max_pontos: int) -> dict[str, list]:
    """Tracado aproximado, ligando os sinistros do segmento em ordem de km.

    Recuo para os trechos sem geometria oficial. Coordenadas repetidas em
    sequencia sao descartadas, e a lista e amostrada para no maximo `max_pontos`.
    """
    cursor = con.execute(
        "SELECT a.codigo_segmento AS codigo, o.latitude, o.longitude "
        "  FROM ocorrencias o JOIN ancoragem a ON a.id = o.id "
        " WHERE o.uf = :uf AND a.codigo_segmento IS NOT NULL "
        "   AND o.latitude IS NOT NULL AND o.longitude IS NOT NULL "
        " ORDER BY a.codigo_segmento, o.km",
        {"uf": uf},
    )
    pontos: dict[str, list] = {}
    for cod, lat, lng in cursor:
        seq = pontos.setdefault(cod, [])
        if not seq or seq[-1] != [lat, lng]:
            seq.append([lat, lng])
    return {cod: _amostrar(seq, max_pontos) for cod, seq in pontos.items()}


def geometria_segmentos(con: sqlite3.Connection, uf: str, *,
                        max_pontos: int = 40) -> list[dict]:
    """Cada segmento com as suas estatisticas e o seu tracado no mapa.

    O tracado preferido e o oficial do SNV, casado pelo codigo. Onde a geometria
    oficial nao existe, a consulta recua para a aproximacao por sinistros. Cada
    item declara a fonte do tracado, para que o mapa nao apresente aproximacao
    como se fosse a via oficial.
    """
    stats = {l["codigo"]: l for l in segmentos_criticos(con, uf, limite=100_000)}
    oficial = _geometria_oficial(con, uf)
    aprox = _geometria_por_sinistros(con, uf, max_pontos)

    itens = []
    for cod, s in stats.items():
        item = dict(s)
        if cod in oficial:
            item["pontos"] = oficial[cod]
            item["fonte_geometria"] = "SNV/DNIT"
        else:
            item["pontos"] = aprox.get(cod, [])
            item["fonte_geometria"] = "aproximacao"
        itens.append(item)
    return itens


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
