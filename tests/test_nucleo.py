"""Testes do nucleo parametrizado. Logica pura, sem os arquivos grandes de dados."""
from __future__ import annotations

import pytest

from custo_social_core import (
    config,
    custo,
    exposicao,
    pipeline,
    referenciamento,
    subregistro,
)


# --- referenciamento ---

def test_safra_casa_com_ano_do_sinistro():
    safras = ["201811A", "202001A", "202101A", "202501A"]
    assert referenciamento.selecionar_safra(2019, safras) == "201811A"
    assert referenciamento.selecionar_safra(2020, safras) == "202001A"
    assert referenciamento.selecionar_safra(2026, safras) == "202501A"


def test_safra_anterior_a_qualquer_disponivel_falha():
    with pytest.raises(ValueError):
        referenciamento.selecionar_safra(2010, ["201811A"])


def test_ancoragem_por_faixa_de_km():
    segs = [
        referenciamento.SegmentoSNV("202001A", 101, "RN", 0.0, 10.0, 10.0),
        referenciamento.SegmentoSNV("202001A", 101, "RN", 10.0, 25.0, 15.0),
    ]
    seg = referenciamento.ancorar(101, "RN", 12.3, segs)
    assert seg.km_inicial == 10.0


def test_km_fora_da_faixa_nao_aproxima():
    segs = [referenciamento.SegmentoSNV("202001A", 101, "RN", 0.0, 10.0, 10.0)]
    with pytest.raises(referenciamento.ForaDaFaixa):
        referenciamento.ancorar(101, "RN", 40.0, segs)


# --- custo em quatro categorias ---

def test_custo_soma_por_gravidade():
    # 2 leves e 1 grave, em ocorrencia com vitimas feridas (R$ dez/2014)
    total = custo.custo_pessoas({"ferido_leve": 2, "ferido_grave": 1}, "com_vitimas")
    assert total == pytest.approx(2 * 8_469.44 + 125_133.91, abs=0.01)


def test_institucional_entra_uma_vez_por_ocorrencia():
    r = custo.custo_ocorrencia({}, "sem_vitimas", aplicar_deflator=False)
    assert r.subtotal_institucional == pytest.approx(453.35, abs=0.01)
    assert r.total == pytest.approx(453.35, abs=0.01)


# --- exposicao ---

def test_custo_por_exposicao_separa_volume_de_risco():
    # mesmo custo, um trecho movimentado e outro vazio: a criticidade por
    # exposicao do trecho vazio e maior.
    movimentado = exposicao.criticidade(1_000_000, vmda=20000, extensao=10)
    vazio = exposicao.criticidade(1_000_000, vmda=2000, extensao=10)
    assert vazio > movimentado


def test_exposicao_nula_devolve_nulo_declarado():
    # nulo declarado, e nao excecao: o segmento segue no ranque por km
    assert exposicao.criticidade(1000.0, vmda=0, extensao=10) is None


# --- subregistro ---

def test_correcao_de_subregistro_por_cenario():
    assert subregistro.corrigir(100.0, "piso") == 100.0
    assert subregistro.corrigir(100.0, "central") == pytest.approx(140.0)
    assert subregistro.corrigir(100.0, "teto") == pytest.approx(196.0)


def test_cenario_invalido_falha():
    with pytest.raises(KeyError):
        subregistro.fator("inexistente")


# --- pipeline (com provedor falso) ---

class ProvedorFalso:
    """Dados minimos de um trecho da BR-101/RN, para exercitar o orquestrador."""

    def safras_snv(self):
        return ["201811A", "202001A"]

    def segmentos_snv(self, safra, uf):
        return [referenciamento.SegmentoSNV(safra, 101, uf, 0.0, 20.0, 20.0)]

    def sinistros(self, uf):
        return [
            {"br": 101, "km": 5.0, "ano": 2020, "gravidade_ocorrencia": "com_vitimas",
             "vetor_c": {"ferido_leve": 1, "Automóvel": 1}},
            {"br": 101, "km": 8.0, "ano": 2020, "gravidade_ocorrencia": "com_fatalidade",
             "vetor_c": {"obito": 1, "Motocicleta": 1}},
        ]

    def vmda_segmento(self, safra, br, km_inicial):
        return 10000.0


def test_pipeline_rn_agrega_por_segmento_e_calcula_criticidade():
    res = pipeline.rodar(ProvedorFalso(), uf="RN")
    assert res.uf == "RN"
    assert len(res.segmentos) == 1
    seg = res.segmentos[0]
    # 1 ocorrencia com ferido leve + 1 com obito, ambas valoradas pelo vetor M
    esperado = (
        custo.custo_ocorrencia({"ferido_leve": 1, "Automóvel": 1}, "com_vitimas").total
        + custo.custo_ocorrencia({"obito": 1, "Motocicleta": 1}, "com_fatalidade").total
    )
    assert seg.custo_social == pytest.approx(esperado, abs=0.01)
    assert seg.corredor_destaque is True                # BR-101 e corredor do RN
    assert seg.custo_por_exposicao is not None          # tem VMDa
    assert seg.custo_corrigido > seg.custo_social       # cenario central (1,4)


def test_pipeline_e_parametrizado_por_uf():
    # a mesma chamada com outra UF nao destaca a BR-101 como corredor do RN
    res = pipeline.rodar(ProvedorFalso(), uf="PB")
    assert res.uf == "PB"
    assert res.segmentos[0].corredor_destaque is False
