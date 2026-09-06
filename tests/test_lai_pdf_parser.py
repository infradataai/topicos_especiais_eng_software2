import pytest

from src.lai_pdf_parser import TabelaVazia, normalizar_linhas


def test_normaliza_cabecalho_e_dados():
    linhas = [["UF", "Beneficios"], ["RN", "1200"], ["PB", "980"]]
    regs = normalizar_linhas(linhas)
    assert regs == [{"UF": "RN", "Beneficios": "1200"}, {"UF": "PB", "Beneficios": "980"}]


def test_ignora_linhas_vazias():
    linhas = [["UF", "Beneficios"], ["", ""], ["RN", "1200"]]
    regs = normalizar_linhas(linhas)
    assert regs == [{"UF": "RN", "Beneficios": "1200"}]


def test_completa_celulas_faltantes():
    linhas = [["UF", "Beneficios", "Ano"], ["RN", "1200"]]
    regs = normalizar_linhas(linhas)
    assert regs == [{"UF": "RN", "Beneficios": "1200", "Ano": ""}]


def test_tabela_sem_dados_levanta():
    with pytest.raises(TabelaVazia):
        normalizar_linhas([["UF", "Beneficios"]])
