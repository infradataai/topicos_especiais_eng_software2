"""Testes da exposicao de trafego (PNCT/VMDa) e da criticidade por exposicao.

Cenarios de openspec/changes/exposicao-e-saude/specs/exposicao/spec.md.
Escritos ANTES da implementacao.
"""
from __future__ import annotations

import pandas as pd
import pytest

from custo_social_core import exposicao as exp

COLS = ["vl_codigo", "vl_br", "sg_uf", "vl_km_inic", "vl_km_fina", "vl_extensa",
        "VMDa_C", "VMDa_D"]


def arquivo_vmda(caminho, linhas, aba="VMDa2025_SNV202401A", com_metadados=True):
    """Reproduz o arquivo do PNCT: aba de metadados mais a aba de dados."""
    with pd.ExcelWriter(caminho) as w:
        if com_metadados:
            pd.DataFrame({"Nome do Campo": ["ID"], "Descrição": ["chave"]}).to_excel(
                w, sheet_name="Metadados", index=False)
        pd.DataFrame(linhas, columns=COLS).to_excel(w, sheet_name=aba, index=False)
    return caminho


def linha(codigo="101BRN0020", c=701.0, d=796.0, ext=14.3):
    return [codigo, 101, "RN", 6.1, 20.4, ext, c, d]


# --- Requisito: leitura do arquivo anual do VMDa ---

def test_reconhece_aba_de_dados_por_conteudo(tmp_path):
    f = arquivo_vmda(tmp_path / "VMDa_2025.xlsx", [linha()])
    d = exp.ler_vmda(f)
    assert len(d) == 1
    assert d.iloc[0]["codigo"] == "101BRN0020"


def test_arquivo_sem_aba_de_dados_falha(tmp_path):
    f = tmp_path / "so_metadados.xlsx"
    pd.DataFrame({"Nome do Campo": ["ID"]}).to_excel(f, sheet_name="Metadados", index=False)
    with pytest.raises(exp.AbaDeDadosAusente):
        exp.ler_vmda(f)


# --- Requisito: volume nos dois sentidos ---

def test_soma_os_dois_sentidos():
    v, completo = exp.volume_total(701.0, 796.0)
    assert v == pytest.approx(1497.0)
    assert completo is True


def test_um_sentido_ausente_usa_o_presente_e_declara():
    v, completo = exp.volume_total(701.0, None)
    assert v == pytest.approx(701.0)
    assert completo is False


def test_sem_medicao_devolve_nulo_declarado():
    v, completo = exp.volume_total(None, None)
    assert v is None
    assert completo is False


# --- Requisito: agregacao de multiplos postos ---

def test_agrega_postos_pela_media_e_conta_quantos(tmp_path):
    f = arquivo_vmda(tmp_path / "VMDa_2024.xlsx",
                     [linha(c=701.0, d=796.0), linha(c=814.0, d=910.0)])
    d = exp.agregar_por_segmento(exp.ler_vmda(f))
    assert len(d) == 1
    r = d.iloc[0]
    assert r["vmda"] == pytest.approx((1497.0 + 1724.0) / 2)   # 1610,5
    assert r["n_postos"] == 2


# --- Requisito: exposicao anual e criticidade ---

def test_exposicao_anual_em_veiculos_km():
    assert exp.veiculos_km_ano(1497.0, 14.3) == pytest.approx(1497.0 * 14.3 * 365)


def test_trecho_vazio_tem_criticidade_maior():
    movimentado = exp.criticidade(1_000_000.0, vmda=20_000.0, extensao=10.0)
    vazio = exp.criticidade(1_000_000.0, vmda=2_000.0, extensao=10.0)
    assert vazio == pytest.approx(movimentado * 10)


def test_sem_exposicao_nao_sai_do_ranque_por_km():
    assert exp.criticidade(1_000_000.0, vmda=None, extensao=10.0) is None
    assert exp.criticidade(1_000_000.0, vmda=0.0, extensao=10.0) is None
