"""Funcionalidade 1 — Carregador de microdados da LAI para SQLite (camada bronze).

Le um arquivo CSV de microdados da LAI como texto (dtype=str, conforme a leitura
bronze imutavel do projeto), valida as colunas obrigatorias e carrega para uma
tabela SQLite de forma idempotente: recarregar o mesmo arquivo nao duplica linhas.

A idempotencia usa uma coluna tecnica _row_hash com restricao UNIQUE e INSERT OR
IGNORE, o que torna a carga deterministica e reproduzivel.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


class ColunasObrigatoriasAusentes(Exception):
    """Levantada quando o arquivo nao tem todas as colunas obrigatorias."""


def _hash_linha(valores) -> str:
    return hashlib.sha1("||".join(valores).encode("utf-8")).hexdigest()


def _identificador_fonte(valor: str) -> str:
    """Return a stable identifier for a source name."""
    return valor.strip()


def _ler_arquivo(caminho: str | Path, configuracao: dict) -> pd.DataFrame:
    caminho = Path(caminho)
    leitura = {"dtype": str}
    if caminho.suffix.lower() == ".csv":
        leitura["sep"] = configuracao.get("sep", ",")
        return pd.read_csv(caminho, keep_default_na=False, **leitura).fillna("")
    if caminho.suffix.lower() == ".xlsx":
        leitura["sheet_name"] = configuracao.get("sheet_name", 0)
        leitura["header"] = configuracao.get("header", 0)
        return pd.read_excel(caminho, **leitura).fillna("")
    raise ValueError("formato nao suportado; use .csv ou .xlsx")


def _checksum(caminho: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(caminho).open("rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(1024 * 1024), b""):
            digest.update(bloco)
    return digest.hexdigest()


def _criar_tabelas(con: sqlite3.Connection) -> None:
    con.executescript(
        """
        CREATE TABLE IF NOT EXISTS fontes (
            fonte TEXT PRIMARY KEY
        );
        CREATE TABLE IF NOT EXISTS lotes (
            lote_id INTEGER PRIMARY KEY AUTOINCREMENT,
            fonte TEXT NOT NULL,
            arquivo TEXT NOT NULL,
            checksum TEXT NOT NULL,
            versao TEXT NOT NULL,
            ingerido_em TEXT NOT NULL,
            configuracao_json TEXT NOT NULL,
            valido INTEGER NOT NULL,
            registros_validos INTEGER NOT NULL,
            registros_invalidos INTEGER NOT NULL,
            idempotente INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (fonte) REFERENCES fontes(fonte)
        );
        CREATE TABLE IF NOT EXISTS bronze_registros (
            lote_id INTEGER NOT NULL,
            linha INTEGER NOT NULL,
            dados_json TEXT NOT NULL,
            PRIMARY KEY (lote_id, linha),
            FOREIGN KEY (lote_id) REFERENCES lotes(lote_id)
        );
        CREATE TABLE IF NOT EXISTS inconsistencias (
            lote_id INTEGER NOT NULL,
            linha INTEGER NOT NULL,
            coluna TEXT NOT NULL,
            regra TEXT NOT NULL,
            valor TEXT NOT NULL,
            FOREIGN KEY (lote_id) REFERENCES lotes(lote_id)
        );
        CREATE TABLE IF NOT EXISTS registros_canonicos (
            registro_id INTEGER PRIMARY KEY AUTOINCREMENT,
            lote_id INTEGER NOT NULL,
            linha_origem INTEGER NOT NULL,
            fingerprint TEXT NOT NULL UNIQUE,
            FOREIGN KEY (lote_id) REFERENCES lotes(lote_id)
        );
        """
    )


def _garantir_colunas_canonicas(
    con: sqlite3.Connection, colunas: list[str]
) -> None:
    existentes = {
        linha[1]
        for linha in con.execute("PRAGMA table_info(registros_canonicos)")
    }
    for coluna in colunas:
        if coluna not in existentes:
            con.execute(f'ALTER TABLE registros_canonicos ADD COLUMN "{coluna}" TEXT')


def _inconsistencias(
    registro: dict[str, str], configuracao: dict, linha: int
) -> list[tuple[int, str, str, str]]:
    problemas = []
    tipos = configuracao.get("types", {})
    for coluna, tipo in tipos.items():
        valor = registro.get(coluna, "")
        invalido = False
        if valor == "":
            continue
        if tipo in {"int", "integer"}:
            try:
                int(valor)
            except (TypeError, ValueError):
                invalido = True
        elif tipo in {"float", "number"}:
            try:
                float(valor.replace(",", "."))
            except (AttributeError, TypeError, ValueError):
                invalido = True
        elif tipo == "date":
            invalido = pd.isna(pd.to_datetime(valor, errors="coerce", dayfirst=True))
        if invalido:
            problemas.append((linha, coluna, f"tipo:{tipo}", valor))

    for regra in configuracao.get("consistency", []):
        coluna = regra["column"]
        valor = registro.get(coluna, "")
        operador = regra.get("operator")
        limite = regra.get("value")
        try:
            comparado = float(valor.replace(",", "."))
            limite = float(limite)
            atende = {
                "min": comparado >= limite,
                "max": comparado <= limite,
            }.get(operador, True)
        except (AttributeError, TypeError, ValueError):
            atende = False
        if not atende:
            problemas.append((linha, coluna, f"consistencia:{operador}", valor))
    return problemas


def ingerir_arquivo(
    caminho: str | Path,
    fonte: str,
    con: sqlite3.Connection,
    configuracao: dict,
) -> dict:
    """Ingere CSV/XLSX, preserva a bronze e consolida registros validos."""
    caminho = Path(caminho)
    fonte = _identificador_fonte(fonte)
    versao = str(configuracao.get("version", ""))
    dados = _ler_arquivo(caminho, configuracao)
    checksum = _checksum(caminho)
    mapeamento = configuracao.get("column_mapping", {})
    obrigatorias = configuracao.get("required_columns", [])
    faltando = [coluna for coluna in obrigatorias if coluna not in dados.columns]
    _criar_tabelas(con)
    con.execute("INSERT OR IGNORE INTO fontes (fonte) VALUES (?)", (fonte,))
    agora = datetime.now(timezone.utc).isoformat()
    con.execute(
        """INSERT INTO lotes
        (fonte, arquivo, checksum, versao, ingerido_em, configuracao_json,
         valido, registros_validos, registros_invalidos)
        VALUES (?, ?, ?, ?, ?, ?, 0, 0, 0)""",
        (fonte, str(caminho), checksum, versao, agora,
         json.dumps(configuracao, sort_keys=True)),
    )
    lote_id = con.execute("SELECT last_insert_rowid()").fetchone()[0]

    for numero, linha in enumerate(dados.to_dict(orient="records"), start=1):
        con.execute(
            "INSERT INTO bronze_registros VALUES (?, ?, ?)",
            (lote_id, numero, json.dumps(linha, ensure_ascii=False, sort_keys=True)),
        )

    problemas = []
    if faltando:
        problemas.extend((0, coluna, "coluna_obrigatoria", "") for coluna in faltando)

    canonicos = []
    colunas_canonicas = list(mapeamento.values())
    _garantir_colunas_canonicas(con, colunas_canonicas)
    for numero, linha in enumerate(dados.to_dict(orient="records"), start=1):
        canonico = {
            destino: str(linha.get(origem, ""))
            for origem, destino in mapeamento.items()
        }
        linha_problemas = _inconsistencias(canonico, configuracao, numero)
        if not faltando and not linha_problemas:
            fingerprint = hashlib.sha256(
                json.dumps(
                    {"fonte": fonte, "versao": versao, "registro": canonico},
                    sort_keys=True,
                    ensure_ascii=False,
                ).encode("utf-8")
            ).hexdigest()
            canonicos.append((numero, fingerprint, canonico))
        problemas.extend(linha_problemas)

    for linha, coluna, regra, valor in problemas:
        con.execute(
            "INSERT INTO inconsistencias VALUES (?, ?, ?, ?, ?)",
            (lote_id, linha, coluna, regra, valor),
        )

    inseridos = 0
    nomes = ["lote_id", "linha_origem", "fingerprint"] + colunas_canonicas
    placeholders = ", ".join("?" for _ in nomes)
    quoted = ", ".join(f'"{nome}"' for nome in nomes)
    for numero, fingerprint, canonico in canonicos:
        valores = [lote_id, numero, fingerprint] + [canonico[coluna] for coluna in colunas_canonicas]
        cur = con.execute(
            f"INSERT OR IGNORE INTO registros_canonicos ({quoted}) VALUES ({placeholders})",
            valores,
        )
        inseridos += cur.rowcount

    invalidos = len(dados) if faltando else len({problema[0] for problema in problemas})
    valido = not problemas
    idempotente = bool(canonicos) and inseridos == 0
    con.execute(
        """UPDATE lotes SET valido = ?, registros_validos = ?,
        registros_invalidos = ?, idempotente = ? WHERE lote_id = ?""",
        (int(valido), inseridos, invalidos, int(idempotente), lote_id),
    )
    con.commit()
    return {
        "lote_id": lote_id,
        "fonte": fonte,
        "arquivo": str(caminho),
        "checksum": checksum,
        "versao": versao,
        "valido": valido,
        "registros_validos": inseridos,
        "registros_invalidos": invalidos,
        "inconsistencias": [
            {"linha": linha, "coluna": coluna, "regra": regra, "valor": valor}
            for linha, coluna, regra, valor in problemas
        ],
        "idempotente": idempotente,
    }


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
