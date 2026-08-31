"""Funcionalidade 2 — Validador de qualidade dos dados carregados da LAI.

Recebe uma tabela SQLite ja carregada e devolve um relatorio de qualidade:
contagem de linhas, colunas ausentes em relacao ao esperado, vazios por coluna,
duplicatas e datas fora de uma faixa. Nao altera os dados, apenas inspeciona.
"""
from __future__ import annotations

import sqlite3


def _colunas(con: sqlite3.Connection, tabela: str) -> list[str]:
    return [r[1] for r in con.execute(f'PRAGMA table_info("{tabela}")')]


def validar_tabela(
    con: sqlite3.Connection,
    tabela: str,
    colunas_esperadas: list[str] | None = None,
    coluna_data: str | None = None,
    ano_min: int | None = None,
    ano_max: int | None = None,
) -> dict:
    """Gera um relatorio de qualidade de uma tabela carregada.

    Args:
        con: conexao SQLite.
        tabela: nome da tabela a validar.
        colunas_esperadas: colunas que deveriam existir (opcional).
        coluna_data: coluna de data a checar por faixa (opcional).
        ano_min, ano_max: faixa de anos aceita para coluna_data.

    Returns:
        Dicionario com as metricas de qualidade.
    """
    cols = [c for c in _colunas(con, tabela) if c != "_row_hash"]
    rel: dict = {"tabela": tabela, "colunas": cols}
    rel["n_linhas"] = con.execute(f'SELECT COUNT(*) FROM "{tabela}"').fetchone()[0]

    if colunas_esperadas is not None:
        rel["colunas_faltando"] = [c for c in colunas_esperadas if c not in cols]

    vazios = {}
    for c in cols:
        vazios[c] = con.execute(
            f'SELECT COUNT(*) FROM "{tabela}" WHERE "{c}" IS NULL OR "{c}" = ""'
        ).fetchone()[0]
    rel["vazios_por_coluna"] = vazios

    if cols:
        expr = ", ".join(f'"{c}"' for c in cols)
        distintas = con.execute(
            f'SELECT COUNT(*) FROM (SELECT DISTINCT {expr} FROM "{tabela}")'
        ).fetchone()[0]
        rel["duplicatas"] = rel["n_linhas"] - distintas

    if coluna_data and coluna_data in cols and ano_min is not None and ano_max is not None:
        fora = con.execute(
            f'SELECT COUNT(*) FROM "{tabela}" '
            f'WHERE CAST(substr("{coluna_data}", 1, 4) AS INTEGER) NOT BETWEEN ? AND ?',
            (ano_min, ano_max),
        ).fetchone()[0]
        rel["datas_fora_da_faixa"] = fora

    rel["ok"] = (
        rel["n_linhas"] > 0
        and not rel.get("colunas_faltando")
        and rel.get("duplicatas", 0) == 0
        and rel.get("datas_fora_da_faixa", 0) == 0
    )
    return rel
