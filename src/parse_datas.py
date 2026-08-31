"""Parsing deterministico de datas do CSV da PRF.

Ver ADR-026 (tese): o CSV da PRF de 2022 traz datas em DD/MM, e o parsing
dependente do ambiente produz contagens diferentes entre maquinas. Fixar
dayfirst=True torna a leitura deterministica, condicao para qualquer
resultado temporal reproduzivel.
"""
from __future__ import annotations

import pandas as pd


def parse_data_prf(serie: pd.Series) -> pd.Series:
    """Converte uma coluna de datas da PRF para datetime de forma deterministica.

    Le sempre com dayfirst=True (dia primeiro), independentemente do locale da
    maquina, e marca valores invalidos como NaT em vez de lancar excecao.

    Args:
        serie: coluna de datas como texto (dtype str), no formato DD/MM/AAAA.

    Returns:
        Serie datetime64[ns]; entradas invalidas viram NaT.
    """
    return pd.to_datetime(serie, dayfirst=True, errors="coerce")
