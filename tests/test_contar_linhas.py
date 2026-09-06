import sqlite3

from src.lai_validador import contar_linhas


def test_contar_linhas():
    con = sqlite3.connect(":memory:")
    con.execute('CREATE TABLE t (a TEXT)')
    con.executemany('INSERT INTO t VALUES (?)', [("x",), ("y",), ("z",)])
    assert contar_linhas(con, "t") == 3
