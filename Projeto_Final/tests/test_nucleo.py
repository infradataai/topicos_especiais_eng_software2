"""Testes do nucleo parametrizado. Logica pura, sem os arquivos grandes de dados."""
from __future__ import annotations

import pytest

from Projeto_Final.custo_social_core import (
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
    tabela = custo.CustoVitima(sem_feridos=40000.0, ferido_leve=20000.0,
                               ferido_grave=120000.0, obito=1250000.0)
    # ocorrencia com 2 leves e 1 grave, sem obito, sem dano avulso
    total = custo.custo_ocorrencia(2, 1, 0, houve_dano=False, tabela=tabela)
    assert total == 2 * 20000.0 + 1 * 120000.0


def test_dano_material_so_entra_sem_vitima():
    tabela = custo.CustoVitima(40000.0, 20000.0, 120000.0, 1250000.0)
    com_vitima = custo.custo_ocorrencia(1, 0, 0, houve_dano=True, tabela=tabela)
    sem_vitima = custo.custo_ocorrencia(0, 0, 0, houve_dano=True, tabela=tabela)
    assert com_vitima == 20000.0          # dano nao soma quando ha vitima
    assert sem_vitima == 40000.0          # dano entra quando nao ha vitima


def test_triangulacao_aceita_dentro_da_tolerancia():
    assert custo.validar_triangulacao(190000.0) is True     # ~4% do Ipea
    assert custo.validar_triangulacao(300000.0) is False    # muito acima


# --- exposicao ---

def test_custo_por_exposicao_separa_volume_de_risco():
    # mesmo custo, um trecho movimentado e outro vazio: a criticidade por
    # exposicao do trecho vazio e maior.
    movimentado = exposicao.custo_por_exposicao(1_000_000, vmda=20000, extensao_km=10)
    vazio = exposicao.custo_por_exposicao(1_000_000, vmda=2000, extensao_km=10)
    assert vazio > movimentado


def test_exposicao_nula_nao_divide():
    with pytest.raises(ValueError):
        exposicao.custo_por_exposicao(1000.0, vmda=0, extensao_km=10)


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
            {"br": 101, "km": 5.0, "ano": 2020, "n_leves": 1, "n_graves": 0,
             "n_mortos": 0, "houve_dano": False},
            {"br": 101, "km": 8.0, "ano": 2020, "n_leves": 0, "n_graves": 0,
             "n_mortos": 1, "houve_dano": False},
        ]

    def vmda_segmento(self, safra, br, km_inicial):
        return 10000.0

    def tabela_custo_vitima(self, uf):
        return custo.CustoVitima(40000.0, 20000.0, 120000.0, 1250000.0)


def test_pipeline_rn_agrega_por_segmento_e_calcula_criticidade():
    res = pipeline.rodar(ProvedorFalso(), uf="RN")
    assert res.uf == "RN"
    assert len(res.segmentos) == 1
    seg = res.segmentos[0]
    assert seg.custo_social == 20000.0 + 1250000.0     # 1 leve + 1 obito
    assert seg.corredor_destaque is True                # BR-101 e corredor do RN
    assert seg.custo_por_exposicao is not None          # tem VMDa
    assert seg.custo_corrigido > seg.custo_social       # cenario central (1,4)


def test_pipeline_e_parametrizado_por_uf():
    # a mesma chamada com outra UF nao destaca a BR-101 como corredor do RN
    res = pipeline.rodar(ProvedorFalso(), uf="PB")
    assert res.uf == "PB"
    assert res.segmentos[0].corredor_destaque is False
