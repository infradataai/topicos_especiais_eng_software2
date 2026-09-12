import sqlite3

from src.analise import analisar_coluna


def _con_com(valores):
    con = sqlite3.connect(":memory:")
    con.execute('CREATE TABLE consolidado (valor TEXT)')
    con.executemany(
        "INSERT INTO consolidado (valor) VALUES (?)",
        [(valor,) for valor in valores],
    )
    con.commit()
    return con


def test_calcula_metricas_descritivas():
    con = _con_com(["10", "20", "30"])

    relatorio = analisar_coluna(con, "consolidado", "valor")

    assert relatorio["n_validos"] == 3
    assert relatorio["n_invalidos"] == 0
    assert relatorio["media"] == 20
    assert relatorio["mediana"] == 20
    assert relatorio["desvio_padrao"] == 10


def test_conta_invalidos_e_os_exclui_das_metricas():
    con = _con_com(["10", "", "texto", "20"])

    relatorio = analisar_coluna(con, "consolidado", "valor")

    assert relatorio["n_validos"] == 2
    assert relatorio["n_invalidos"] == 2
    assert relatorio["media"] == 15


def test_detecta_outlier_com_iqr():
    con = _con_com(["10", "11", "12", "13", "100"])

    relatorio = analisar_coluna(con, "consolidado", "valor")

    assert relatorio["limite_superior"] == 16
    assert relatorio["outliers"] == [{"id": 5, "valor": 100.0}]


def test_nao_detecta_outlier_e_nao_altera_tabela():
    con = _con_com(["10", "20", "30"])
    antes = con.execute("SELECT rowid, valor FROM consolidado").fetchall()

    relatorio = analisar_coluna(con, "consolidado", "valor")

    depois = con.execute("SELECT rowid, valor FROM consolidado").fetchall()
    assert relatorio["outliers"] == []
    assert depois == antes
