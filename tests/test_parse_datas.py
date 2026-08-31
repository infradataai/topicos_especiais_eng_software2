import pandas as pd

from src.parse_datas import parse_data_prf


def test_dayfirst_interpreta_dia_primeiro():
    # 03/02/2022 deve ser 3 de fevereiro, nao 2 de marco
    r = parse_data_prf(pd.Series(["03/02/2022"]))
    assert r.iloc[0] == pd.Timestamp("2022-02-03")


def test_valor_invalido_vira_nat():
    r = parse_data_prf(pd.Series(["data ruim"]))
    assert pd.isna(r.iloc[0])


def test_determinismo_dia_primeiro():
    # 13/01 e dia 13; 01/13 nao existe (mes 13) -> NaT
    r = parse_data_prf(pd.Series(["13/01/2022", "01/13/2022"]))
    assert r.iloc[0] == pd.Timestamp("2022-01-13")
    assert pd.isna(r.iloc[1])
