"""Testes dos agregados do DATASUS: obitos do SIM e internacoes do SIH.

Cenarios de openspec/changes/exposicao-e-saude/specs/saude/spec.md.
Escritos ANTES da implementacao.
"""
from __future__ import annotations

import pandas as pd
import pytest

from custo_social_core import saude


# --- Requisito: leitura dos agregados do DATASUS ---

def test_le_csv_com_marca_de_ordem_de_byte(tmp_path):
    """Os agregados do DATASUS vem com BOM; sem tratar, a 1a coluna vira '﻿uf'."""
    f = tmp_path / "obitos.csv"
    f.write_bytes("uf,ano,obitos_transporte\nRN,2024,509\n".encode("utf-8-sig"))
    d = saude.ler_agregado(f)
    assert list(d.columns)[0] == "uf"
    assert "﻿" not in "".join(d.columns)


# --- Requisito: obitos por acidente de transporte ---

def test_obitos_por_uf_e_ano(tmp_path):
    f = tmp_path / "sim.csv"
    f.write_bytes(
        "uf,ano,obitos_transporte,obito_estab_saude,obito_via_publica\n"
        "RN,2024,509,249,237\nPB,2024,400,200,180\n".encode("utf-8-sig"))
    d = saude.ler_agregado(f)
    r = saude.obitos(d, uf="RN", ano=2024)
    assert r["obitos_transporte"] == 509
    assert r["obito_estab_saude"] == 249
    assert r["obito_via_publica"] == 237


# --- Requisito: internacoes por causa externa ---

def test_soma_internacoes_do_ano(tmp_path):
    f = tmp_path / "sih.csv"
    linhas = "".join(f"RN,2024,{m:02d},100\n" for m in range(1, 13))
    f.write_bytes(("uf,ano,mes,internacoes\n" + linhas).encode("utf-8-sig"))
    d = saude.ler_agregado(f)
    assert saude.internacoes_do_ano(d, uf="RN", ano=2024) == 1200


# --- Requisito: cobertura da PRF sobre o SIM ---

def test_calcula_cobertura_de_jurisdicao():
    prf = pd.DataFrame([{"uf": "RN", "ano": 2024, "obitos_prf": 118}])
    sim = pd.DataFrame([{"uf": "RN", "ano": 2024, "obitos_transporte": 509}])
    r = saude.cobertura_jurisdicao(prf, sim)
    linha = r.iloc[0]
    assert linha["cobertura_jurisdicao"] == pytest.approx(118 / 509, abs=1e-6)
    assert linha["rotulo"] == "cobertura de jurisdicao"


def test_recusa_usar_cobertura_como_subregistro():
    prf = pd.DataFrame([{"uf": "RN", "ano": 2024, "obitos_prf": 118}])
    sim = pd.DataFrame([{"uf": "RN", "ano": 2024, "obitos_transporte": 509}])
    r = saude.cobertura_jurisdicao(prf, sim)
    with pytest.raises(saude.UsoIndevidoDeCobertura):
        saude.como_fator_de_subregistro(r)
