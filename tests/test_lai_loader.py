import sqlite3

import pandas as pd
import pytest

from src.lai_loader import (
    ColunasObrigatoriasAusentes,
    carregar_csv_lai,
    ingerir_arquivo,
)

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


def _configuracao():
    return {
        "version": "2026-01",
        "required_columns": ["competencia", "valor"],
        "column_mapping": {"competencia": "periodo", "valor": "valor"},
        "types": {"periodo": "string", "valor": "float"},
    }


def test_inge_representacoes_de_dois_orgaos(tmp_path):
    csv = _csv(tmp_path, "competencia,valor\n2026-01,10.5\n")
    xlsx = tmp_path / "orgao_b.xlsx"
    pd.DataFrame({"mes": ["2026-02"], "montante": [20.5]}).to_excel(xlsx, index=False)
    con = sqlite3.connect(":memory:")

    rel_a = ingerir_arquivo(csv, "orgao-a", con, _configuracao())
    config_b = {
        **_configuracao(),
        "required_columns": ["mes", "montante"],
        "column_mapping": {"mes": "periodo", "montante": "valor"},
    }
    rel_b = ingerir_arquivo(xlsx, "orgao-b", con, config_b)

    assert rel_a["valido"] is True
    assert rel_b["valido"] is True
    assert con.execute("SELECT COUNT(*) FROM registros_canonicos").fetchone()[0] == 2
    origem = con.execute(
        "SELECT fontes.fonte, lotes.versao FROM registros_canonicos "
        "JOIN lotes USING (lote_id) JOIN fontes USING (fonte) "
        "WHERE registros_canonicos.valor = '20.5'"
    ).fetchone()
    assert origem == ("orgao-b", "2026-01")


def test_inge_tipo_invalido_sem_consolidar(tmp_path):
    csv = _csv(tmp_path, "competencia,valor\n2026-01,nao-numero\n")
    con = sqlite3.connect(":memory:")

    relatorio = ingerir_arquivo(csv, "orgao-a", con, _configuracao())

    assert relatorio["valido"] is False
    assert relatorio["registros_invalidos"] == 1
    assert relatorio["inconsistencias"][0]["coluna"] == "valor"
    assert con.execute("SELECT COUNT(*) FROM registros_canonicos").fetchone()[0] == 0
    assert con.execute("SELECT COUNT(*) FROM bronze_registros").fetchone()[0] == 1


def test_inge_reprocessamento_e_idempotente(tmp_path):
    csv = _csv(tmp_path, "competencia,valor\n2026-01,10.5\n")
    con = sqlite3.connect(":memory:")

    primeira = ingerir_arquivo(csv, "orgao-a", con, _configuracao())
    segunda = ingerir_arquivo(csv, "orgao-a", con, _configuracao())

    assert primeira["registros_validos"] == 1
    assert segunda["registros_validos"] == 0
    assert segunda["idempotente"] is True
    assert con.execute("SELECT COUNT(*) FROM registros_canonicos").fetchone()[0] == 1
