import sqlite3

import pytest

from src.lai_loader import ColunasObrigatoriasAusentes, carregar_csv_lai

OBRIG = ["competencia", "especie", "valor"]


def _csv(tmp_path, conteudo):
    p = tmp_path / "lai.csv"
    p.write_text(conteudo, encoding="utf-8")
    return p


def test_carrega_linhas(tmp_path):
    csv = _csv(tmp_path, "competencia,especie,valor\n2022-01,91,1500\n2022-01,92,2000\n")
    con = sqlite3.connect(":memory:")
    n = carregar_csv_lai(csv, con, "bronze_lai", OBRIG)
    assert n == 2
    assert con.execute("SELECT COUNT(*) FROM bronze_lai").fetchone()[0] == 2


def test_idempotente_nao_duplica(tmp_path):
    csv = _csv(tmp_path, "competencia,especie,valor\n2022-01,91,1500\n")
    con = sqlite3.connect(":memory:")
    assert carregar_csv_lai(csv, con, "bronze_lai", OBRIG) == 1
    # recarregar o mesmo arquivo nao insere de novo
    assert carregar_csv_lai(csv, con, "bronze_lai", OBRIG) == 0
    assert con.execute("SELECT COUNT(*) FROM bronze_lai").fetchone()[0] == 1


def test_coluna_faltando_levanta(tmp_path):
    csv = _csv(tmp_path, "competencia,especie\n2022-01,91\n")  # falta "valor"
    con = sqlite3.connect(":memory:")
    with pytest.raises(ColunasObrigatoriasAusentes):
        carregar_csv_lai(csv, con, "bronze_lai", OBRIG)


def test_arquivo_vazio_retorna_zero(tmp_path):
    csv = _csv(tmp_path, "competencia,especie,valor\n")  # so cabecalho
    con = sqlite3.connect(":memory:")
    assert carregar_csv_lai(csv, con, "bronze_lai", OBRIG) == 0
