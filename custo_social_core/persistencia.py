"""Consolidacao em banco relacional unico (SQLite), com proveniencia.

A carga e idempotente pela chave de cada grao, e cada carga registra o orgao de
origem, o arquivo, a referencia (safra ou ano) e o instante. O banco fica na
pasta de dados, fora do controle de versao.

Spec em openspec/changes/consolidacao-e-snv/specs/persistencia/.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from sqlalchemy import (Column, Float, Integer, MetaData, String, Table, create_engine,
                        func, select, text)
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

metadata = MetaData()

ocorrencias = Table(
    "ocorrencias", metadata,
    Column("id", String, primary_key=True),
    Column("uf", String), Column("br", Integer), Column("km", Float),
    Column("data", String), Column("ano", Integer), Column("mes", Integer),
    Column("classificacao_acidente", String),
    Column("latitude", Float), Column("longitude", Float),
)
veiculos = Table(
    "veiculos", metadata,
    Column("id", String, primary_key=True),
    Column("id_veiculo", String, primary_key=True),
    Column("tipo_veiculo", String), Column("classe_ipea", String),
)
pessoas = Table(
    "pessoas", metadata,
    Column("id", String, primary_key=True),
    Column("pesid", String, primary_key=True),
    Column("gravidade", String), Column("idade", Integer),
    Column("sexo", String), Column("tipo_envolvido", String),
)
causas_tipos = Table(
    "causas_tipos", metadata,
    Column("id", String, primary_key=True),
    Column("causa_acidente", String, primary_key=True),
    Column("tipo_acidente", String, primary_key=True),
)
segmentos_snv = Table(
    "segmentos_snv", metadata,
    Column("safra", String, primary_key=True),
    Column("codigo", String, primary_key=True),
    Column("br", Integer), Column("uf", String),
    Column("km_inicial", Float), Column("km_final", Float), Column("extensao", Float),
    Column("administracao", String), Column("jurisdicao", String),
    Column("tipo_trecho", String), Column("regime", String),
)
custo_ocorrencia = Table(
    "custo_ocorrencia", metadata,
    Column("id", String, primary_key=True),
    Column("total", Float), Column("subtotal_pessoas", Float),
    Column("subtotal_veiculos", Float), Column("subtotal_institucional", Float),
    Column("categoria", String), Column("base_monetaria", String),
)
ancoragem = Table(
    "ancoragem", metadata,
    Column("id", String, primary_key=True),
    Column("safra", String), Column("codigo_segmento", String),
    Column("houve_desempate", Integer), Column("motivo", String),
)
exposicao_segmento = Table(
    "exposicao_segmento", metadata,
    Column("ano", Integer, primary_key=True),
    Column("codigo", String, primary_key=True),
    Column("br", Integer), Column("uf", String), Column("extensao", Float),
    Column("vmda", Float), Column("n_postos", Integer),
    Column("sentidos_completos", Integer), Column("safra_vmda", String),
)
obitos_sim = Table(
    "obitos_sim", metadata,
    Column("uf", String, primary_key=True),
    Column("ano", Integer, primary_key=True),
    Column("obitos_transporte", Integer),
    Column("obito_estab_saude", Integer), Column("obito_via_publica", Integer),
)
internacoes_sih = Table(
    "internacoes_sih", metadata,
    Column("uf", String, primary_key=True),
    Column("ano", Integer, primary_key=True),
    Column("mes", Integer, primary_key=True),
    Column("internacoes", Integer),
)
proveniencia_t = Table(
    "proveniencia", metadata,
    Column("tabela", String, primary_key=True),
    Column("arquivo", String, primary_key=True),
    Column("orgao", String), Column("referencia", String),
    Column("carregado_em", String),
)

TABELAS = {t.name: t for t in metadata.tables.values()}


def caminho_banco_padrao() -> Path:
    """Caminho do banco consolidado, dentro da pasta de dados (fora do git)."""
    return Path(__file__).resolve().parent.parent / "dados" / "consolidado.db"


def criar_esquema(caminho: str | Path):
    """Cria o banco e as tabelas, se ainda nao existirem."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    eng = create_engine(f"sqlite:///{caminho}")
    metadata.create_all(eng)
    return eng


def _para_sqlite(v):
    """Converte tipos do pandas e do numpy para os que o SQLite aceita vincular.

    Timestamp vira texto ISO, tipos do numpy viram nativos do Python, e ausente
    vira nulo. Sem isso a carga falha ao vincular a coluna de data.
    """
    if v is None or (not isinstance(v, (list, dict, str)) and pd.isna(v)):
        return None
    if isinstance(v, pd.Timestamp):
        return v.isoformat()
    if hasattr(v, "item"):          # numpy int64, float64, bool_
        return v.item()
    return v


def contar(engine, tabela: str) -> int:
    """Conta as linhas de uma tabela."""
    with engine.connect() as c:
        return c.execute(select(func.count()).select_from(TABELAS[tabela])).scalar_one()


def carregar(engine, tabela: str, df: pd.DataFrame, *, orgao: str,
             arquivo: str, referencia: str) -> int:
    """Carrega um DataFrame, sem duplicar pela chave, e registra a proveniencia.

    A insercao ignora conflito de chave primaria, o que torna a repeticao
    inofensiva. Apagar e recarregar foi descartado: perderia a proveniencia das
    cargas anteriores.

    Returns:
        Quantas linhas foram efetivamente inseridas.
    """
    t = TABELAS[tabela]
    colunas = {c.name for c in t.columns}
    sub = df[[c for c in df.columns if c in colunas]]
    registros = [
        {k: _para_sqlite(v) for k, v in linha.items()}
        for linha in sub.to_dict("records")
    ]
    antes = contar(engine, tabela)
    if registros:
        with engine.begin() as c:
            c.execute(sqlite_insert(t).prefix_with("OR IGNORE"), registros)
    inseridas = contar(engine, tabela) - antes

    with engine.begin() as c:
        c.execute(
            sqlite_insert(proveniencia_t).prefix_with("OR REPLACE"),
            [{"tabela": tabela, "arquivo": arquivo, "orgao": orgao,
              "referencia": referencia,
              "carregado_em": datetime.now(timezone.utc).isoformat(timespec="seconds")}],
        )
    return inseridas


def proveniencia(engine, tabela: str | None = None) -> pd.DataFrame:
    """Devolve o registro de proveniencia, de uma tabela ou de todas."""
    q = select(proveniencia_t)
    if tabela is not None:
        q = q.where(proveniencia_t.c.tabela == tabela)
    with engine.connect() as c:
        return pd.DataFrame(c.execute(q).mappings().all())


def custo_por_segmento(engine, uf: str) -> pd.DataFrame:
    """Custo social agregado por segmento, para uma unidade da federacao."""
    # Uma linha por segmento: o custo soma todas as safras ancoradas, e a extensao
    # vem da safra mais recente. Agrupar por (codigo, safra) somaria a mesma
    # extensao fisica varias vezes e inflaria a malha do estado.
    sql = """
        WITH anc AS (
            SELECT a.id, a.codigo_segmento AS codigo, a.safra
              FROM ancoragem a
              JOIN ocorrencias o ON o.id = a.id
             WHERE o.uf = :uf AND a.codigo_segmento IS NOT NULL
        ),
        recente AS (
            SELECT codigo, MAX(safra) AS safra FROM anc GROUP BY codigo
        ),
        -- a exposicao entra pelo ano mais recente disponivel de cada segmento
        exp AS (
            SELECT codigo, vmda, n_postos
              FROM exposicao_segmento e
             WHERE e.ano = (SELECT MAX(ano) FROM exposicao_segmento
                             WHERE codigo = e.codigo)
        )
        SELECT s.codigo, s.br, s.uf, s.extensao, s.regime, s.jurisdicao,
               SUM(c.total) AS custo_social,
               COUNT(*)     AS ocorrencias,
               MAX(e.vmda)  AS vmda,
               MAX(e.n_postos) AS n_postos
          FROM anc
          JOIN custo_ocorrencia c ON c.id = anc.id
          JOIN recente          r ON r.codigo = anc.codigo
          JOIN segmentos_snv    s ON s.codigo = r.codigo AND s.safra = r.safra
     LEFT JOIN exp             e ON e.codigo = s.codigo
      GROUP BY s.codigo, s.br, s.uf, s.extensao, s.regime, s.jurisdicao
    """
    with engine.connect() as c:
        d = pd.DataFrame(c.execute(text(sql), {"uf": uf}).mappings().all())
    if not d.empty:
        d["custo_por_km"] = d["custo_social"] / d["extensao"]
    return d
