"""Analise descritiva e deteccao de outliers da camada canonica."""
from __future__ import annotations

import sqlite3
import statistics


def _identificador_sql(nome: str) -> str:
    return '"' + nome.replace('"', '""') + '"'


def analisar_coluna(
    con: sqlite3.Connection,
    tabela: str,
    coluna: str,
) -> dict:
    """Calcula metricas descritivas e outliers IQR sem alterar a tabela."""
    tabela_sql = _identificador_sql(tabela)
    coluna_sql = _identificador_sql(coluna)
    linhas = con.execute(
        f"SELECT rowid, {coluna_sql} FROM {tabela_sql}"
    ).fetchall()

    valores = []
    invalidos = 0
    observacoes = []
    for identificador, bruto in linhas:
        try:
            if bruto is None or (isinstance(bruto, str) and not bruto.strip()):
                raise ValueError
            valor = float(bruto)
        except (TypeError, ValueError):
            invalidos += 1
            continue
        valores.append(valor)
        observacoes.append((identificador, valor))

    relatorio = {
        "tabela": tabela,
        "coluna": coluna,
        "n_validos": len(valores),
        "n_invalidos": invalidos,
        "media": statistics.mean(valores) if valores else None,
        "mediana": statistics.median(valores) if valores else None,
        "desvio_padrao": statistics.stdev(valores) if len(valores) >= 2 else None,
        "q1": None,
        "q3": None,
        "limite_inferior": None,
        "limite_superior": None,
        "outliers": [],
    }
    if len(valores) < 2:
        return relatorio

    quartis = statistics.quantiles(valores, n=4, method="inclusive")
    q1, q3 = quartis[0], quartis[2]
    iqr = q3 - q1
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr
    relatorio.update(
        {
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "limite_inferior": limite_inferior,
            "limite_superior": limite_superior,
            "outliers": [
                {"id": identificador, "valor": valor}
                for identificador, valor in observacoes
                if valor < limite_inferior or valor > limite_superior
            ],
        }
    )
    return relatorio
