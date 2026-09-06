import sqlite3

from src.lai_validador import validar_tabela


def _con_com(linhas):
    con = sqlite3.connect(":memory:")
    con.execute('CREATE TABLE t ("competencia" TEXT, "especie" TEXT, "valor" TEXT)')
    con.executemany('INSERT INTO t VALUES (?, ?, ?)', linhas)
    con.commit()
    return con


def test_relatorio_basico():
    con = _con_com([("2022-01", "91", "1500"), ("2022-02", "92", "2000")])
    rel = validar_tabela(con, "t", colunas_esperadas=["competencia", "especie", "valor"])
    assert rel["n_linhas"] == 2
    assert rel["colunas_faltando"] == []
    assert rel["duplicatas"] == 0
    assert rel["ok"] is True


def test_detecta_vazios_e_duplicatas():
    con = _con_com([("2022-01", "", "1500"), ("2022-01", "", "1500")])
    rel = validar_tabela(con, "t")
    assert rel["vazios_por_coluna"]["especie"] == 2
    assert rel["duplicatas"] == 1
    assert rel["ok"] is False


def test_coluna_faltando_e_data_fora_da_faixa():
    con = _con_com([("2030-01", "91", "1500")])
    rel = validar_tabela(
        con, "t",
        colunas_esperadas=["competencia", "especie", "valor", "uf"],
        coluna_data="competencia", ano_min=2019, ano_max=2025,
    )
    assert "uf" in rel["colunas_faltando"]
    assert rel["datas_fora_da_faixa"] == 1
    assert rel["ok"] is False
