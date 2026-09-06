"""Funcionalidade 1 — Carregador de microdados da LAI para SQLite (camada bronze).

Le um arquivo CSV de microdados da LAI como texto (dtype=str, conforme a leitura
bronze imutavel do projeto), valida as colunas obrigatorias e carrega para uma
tabela SQLite de forma idempotente: recarregar o mesmo arquivo nao duplica linhas.

A idempotencia usa uma coluna tecnica _row_hash com restricao UNIQUE e INSERT OR
IGNORE, o que torna a carga deterministica e reproduzivel.
"""
from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path

import pandas as pd


class ColunasObrigatoriasAusentes(Exception):
    """Levantada quando o arquivo nao tem todas as colunas obrigatorias."""


def _hash_linha(valores) -> str:
    return hashlib.sha1("||".join(valores).encode("utf-8")).hexdigest()


def carregar_csv_lai(
    caminho_csv: str | Path,
    con: sqlite3.Connection,
    tabela: str,
    colunas_obrigatorias: list[str],
    sep: str = ",",
) -> int:
    """Carrega um CSV de microdados da LAI para uma tabela SQLite.

    Args:
        caminho_csv: caminho do arquivo CSV.
        con: conexao SQLite aberta.
        tabela: nome da tabela de destino (camada bronze).
        colunas_obrigatorias: colunas que devem existir no arquivo.
        sep: separador do CSV.

    Returns:
        Numero de linhas NOVAS inseridas (0 se o arquivo ja foi carregado).

    Raises:
        ColunasObrigatoriasAusentes: se faltar alguma coluna obrigatoria.
    """
    df = pd.read_csv(caminho_csv, dtype=str, sep=sep).fillna("")

    faltando = [c for c in colunas_obrigatorias if c not in df.columns]
    if faltando:
        raise ColunasObrigatoriasAusentes(f"colunas ausentes: {faltando}")

    if df.empty:
        return 0

    df = df.drop_duplicates().reset_index(drop=True)
    colunas = list(df.columns)
    df["_row_hash"] = [_hash_linha(list(r)) for r in df[colunas].itertuples(index=False)]

    defs = ", ".join(f'"{c}" TEXT' for c in colunas)
    con.execute(
        f'CREATE TABLE IF NOT EXISTS "{tabela}" ({defs}, "_row_hash" TEXT UNIQUE)'
    )

    todas = colunas + ["_row_hash"]
    placeholders = ", ".join("?" * len(todas))
    nomes = ", ".join(f'"{c}"' for c in todas)
    inseridos = 0
    for linha in df[todas].itertuples(index=False):
        cur = con.execute(
            f'INSERT OR IGNORE INTO "{tabela}" ({nomes}) VALUES ({placeholders})',
            tuple(linha),
        )
        inseridos += cur.rowcount
    con.commit()
    return inseridos
