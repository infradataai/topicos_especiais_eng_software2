"""Testes do calculo de custo social (produto escalar C . M).

Cada teste corresponde a um cenario da spec em
openspec/changes/calculo-custo/specs/custo-social/spec.md.
Escritos ANTES da implementacao, conforme o tasks.md.
"""
from __future__ import annotations

import pytest

from custo_social_core import custo

SV, CV, CF = "sem_vitimas", "com_vitimas", "com_fatalidade"


# --- Requisito: selecao da coluna do vetor M pela gravidade da ocorrencia ---

def test_mesma_vitima_custa_diferente_conforme_a_ocorrencia():
    leve_em_cv = custo.custo_pessoas({"ferido_leve": 1}, CV)
    leve_em_cf = custo.custo_pessoas({"ferido_leve": 1}, CF)
    assert leve_em_cv == pytest.approx(8_469.44, abs=0.01)
    assert leve_em_cf == pytest.approx(8_635.77, abs=0.01)


def test_classificacao_desconhecida_falha():
    with pytest.raises(custo.GravidadeDesconhecida):
        custo.custo_pessoas({"ferido_leve": 1}, "com_muitos_feridos")


# --- Requisito: custo associado as pessoas ---

def test_soma_pessoas_de_gravidades_distintas():
    # 2 mortos e 1 ileso, em ocorrencia com fatalidade
    total = custo.custo_pessoas({"obito": 2, "ileso": 1}, CF)
    assert total == pytest.approx(868_413.32, abs=0.01)


def test_gravidade_nao_informada_nao_soma_e_e_declarada():
    r = custo.custo_ocorrencia(
        {"ferido_leve": 1, "nao_informado": 2}, CV, aplicar_deflator=False
    )
    # so a vitima leve soma
    assert r.subtotal_pessoas == pytest.approx(8_469.44, abs=0.01)
    # e a lacuna e declarada no resultado
    assert r.pessoas_sem_gravidade == 2


# --- Requisito: contagem de caminhoes pela regra de composicao ---

def test_cavalo_com_semirreboque_conta_um_caminhao():
    assert custo.contar_caminhoes({"Caminhão-trator": 1, "Semireboque": 1}) == 1


def test_bitrem_conta_um_caminhao():
    # uma tratora puxando duas carretas continua sendo uma composicao
    assert custo.contar_caminhoes({"Caminhão-trator": 1, "Semireboque": 2}) == 1


def test_carreta_sem_tratora_conta_um_caminhao():
    c = custo.contar_caminhoes({"Semireboque": 1, "Automóvel": 1})
    assert c == 1


def test_sem_tratora_e_sem_carreta_nao_conta_caminhao():
    assert custo.contar_caminhoes({"Automóvel": 2}) == 0


# --- Requisito: custo associado aos veiculos ---

def test_motoneta_vale_como_motocicleta():
    total = custo.custo_veiculos({"Motoneta": 1}, CF)
    assert total == pytest.approx(4_269.83, abs=0.01)


def test_tipo_de_veiculo_nao_mapeado_falha():
    with pytest.raises(custo.TipoVeiculoNaoMapeado):
        custo.custo_veiculos({"Nave espacial": 1}, CV)


# --- Requisito: custo institucional ---

def test_ocorrencia_sem_veiculo_tem_so_o_institucional():
    r = custo.custo_ocorrencia({}, SV, aplicar_deflator=False)
    assert r.total == pytest.approx(453.35, abs=0.01)


# --- Requisito: atualizacao monetaria com base unica ---

def test_exemplo_trabalhado_ocorrencia_182341():
    """Regressao de numero fechado: trava a memoria de calculo inteira.

    Ocorrencia 182341, BR-405 km 82,4: 2 obitos, 1 ileso, 1 motoneta, 1 automovel,
    classificada com vitimas fatais.
    """
    vetor_c = {"obito": 2, "ileso": 1, "Motoneta": 1, "Automóvel": 1}
    sem_def = custo.custo_ocorrencia(vetor_c, CF, aplicar_deflator=False)
    com_def = custo.custo_ocorrencia(vetor_c, CF)
    assert sem_def.total == pytest.approx(892_660.12, abs=0.01)
    assert com_def.total == pytest.approx(1_682_487.58, abs=0.01)


def test_deflator_reproduz_parametro_da_v07():
    # 23.498,77 (dez/2014) x 1,884802 = 44.290,53 (jun/2026), como na aba Parametros
    assert custo.para_junho_2026(23_498.77) == pytest.approx(44_290.53, abs=0.01)


# --- Requisito: saida decomposta por categoria ---

def test_ocorrencia_classificada_pela_vitima_mais_grave():
    r = custo.custo_ocorrencia({"ferido_leve": 1, "ferido_grave": 1}, CV)
    assert r.categoria == "com_vitima_grave"
