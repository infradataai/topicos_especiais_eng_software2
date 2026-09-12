"""Testes da leitura do SNV e da ancoragem por referenciamento linear.

Cada teste corresponde a um cenario de
openspec/changes/consolidacao-e-snv/specs/snv-referenciamento/spec.md.
Escritos ANTES da implementacao.
"""
from __future__ import annotations

import pandas as pd
import pytest

from custo_social_core import snv


def planilha_falsa(caminho, linhas):
    """Reproduz o formato do DNIT: duas linhas de metadados e o cabecalho na terceira."""
    cols = ["BR", "UF ", "Tipo de trecho", "Desc Coinc", "Código", "Local de Início",
            "Local de Fim", "km inicial", "km final", "Extensão", "Superfície Federal",
            "Obras", "Federal Coincidente", "Administração", "Ato legal",
            "Estadual Coincidente", "Superfície Est. Coincidente", "Jurisdição",
            "Superfície", "Unidade Local"]
    meta = [[None] * 12 + ["Versão SNV: 202501A"] + [None] * 7,
            [None] * 12 + ["CONTATO: snv@dnit.gov.br"] + [None] * 7]
    corpo = [[l.get(c.strip(), None) for c in cols] for l in linhas]
    pd.DataFrame(meta + [cols] + corpo).to_excel(caminho, header=False, index=False)
    return caminho


def seg(**kw):
    base = {"BR": "101", "UF": "RN", "Tipo de trecho": "Eixo Principal",
            "Código": "101BRN0020", "km inicial": 6.1, "km final": 20.4,
            "Extensão": 14.3, "Administração": "Federal", "Jurisdição": "Federal"}
    base.update(kw)
    return base


# --- Requisito: leitura da planilha do SNV ---

def test_le_safra_e_filtra_uf(tmp_path):
    f = planilha_falsa(tmp_path / "SNV_202501A.xlsx",
                       [seg(), seg(UF="PB", Código="101BPB0010")])
    d = snv.ler_safra(f, uf="RN")
    assert len(d) == 1
    assert set(["br", "uf", "codigo", "km_inicial", "km_final", "extensao",
                "administracao", "jurisdicao"]).issubset(d.columns)


def test_quilometragem_com_virgula_decimal(tmp_path):
    """A safra 202511A grava '2,4'; as anteriores gravam '2.4'.

    Sem normalizar, a safra inteira vira nulo e nenhuma ocorrencia do ano ancora.
    """
    f = planilha_falsa(tmp_path / "SNV_202511A.xlsx", [
        seg(**{"km inicial": "0,0", "km final": "2,4", "Extensão": "2,4"})])
    d = snv.ler_safra(f, uf="RN")
    assert d.iloc[0]["km_inicial"] == pytest.approx(0.0)
    assert d.iloc[0]["km_final"] == pytest.approx(2.4)
    assert d["km_final"].notna().all()


def test_cabecalho_inesperado_falha(tmp_path):
    f = tmp_path / "SNV_ruim.xlsx"
    pd.DataFrame([["a", "b"], ["c", "d"], ["e", "f"]]).to_excel(f, header=False, index=False)
    with pytest.raises(snv.CabecalhoInesperado):
        snv.ler_safra(f)


# --- Requisito: selecao da safra vigente ---

def test_safra_vigente_no_ano_do_sinistro():
    assert snv.selecionar_safra(2020, ["201811A", "202001A", "202501A"]) == "202001A"


def test_sinistro_anterior_a_primeira_safra_falha():
    with pytest.raises(snv.SafraIndisponivel):
        snv.selecionar_safra(2019, ["202001A"])


# --- Requisito: ancoragem por referenciamento linear ---

def segmentos_rn():
    return pd.DataFrame([
        {"br": 101, "uf": "RN", "codigo": "101BRN0020", "km_inicial": 6.1,
         "km_final": 20.4, "extensao": 14.3, "tipo_trecho": "Eixo Principal",
         "administracao": "Federal", "jurisdicao": "Federal"},
        {"br": 101, "uf": "RN", "codigo": "101BRN0025", "km_inicial": 20.4,
         "km_final": 320.0, "extensao": 299.6, "tipo_trecho": "Eixo Principal",
         "administracao": "Federal", "jurisdicao": "Federal"},
    ])


def test_ancora_km_dentro_da_faixa():
    a = snv.ancorar(101, "RN", 12.5, segmentos_rn())
    assert a.ancorada is True
    assert a.codigo == "101BRN0020"
    assert a.houve_desempate is False


def test_km_fora_da_faixa_nao_ancora_e_registra_motivo():
    a = snv.ancorar(101, "RN", 400.0, segmentos_rn())
    assert a.ancorada is False
    assert a.codigo is None
    assert "fora" in a.motivo.lower()


# --- Requisito: desempate de trechos coincidentes ---

def test_desempate_entre_segmentos_coincidentes():
    coincidentes = pd.DataFrame([
        {"br": 101, "uf": "RN", "codigo": "101BRN0100", "km_inicial": 40.0,
         "km_final": 60.0, "extensao": 20.0, "tipo_trecho": "Eixo Principal",
         "administracao": "Federal", "jurisdicao": "Federal"},
        {"br": 101, "uf": "RN", "codigo": "101BRN0200", "km_inicial": 45.0,
         "km_final": 55.0, "extensao": 10.0, "tipo_trecho": "Contorno",
         "administracao": "Federal", "jurisdicao": "Federal"},
    ])
    a = snv.ancorar(101, "RN", 50.0, coincidentes)
    assert a.ancorada is True
    assert a.houve_desempate is True
    # o eixo principal tem preferencia sobre o contorno, mesmo sendo mais extenso
    assert a.codigo == "101BRN0100"


def test_desempate_prefere_jurisdicao_federal():
    """A PRF cobre malha federal; ancorar num estadual coincidente contamina o regime."""
    coincidentes = pd.DataFrame([
        {"br": 101, "uf": "RN", "codigo": "101BRN0300", "km_inicial": 40.0,
         "km_final": 60.0, "extensao": 20.0, "tipo_trecho": "Eixo Principal",
         "administracao": "Federal", "jurisdicao": "Federal"},
        {"br": 101, "uf": "RN", "codigo": "101BRN0400", "km_inicial": 45.0,
         "km_final": 55.0, "extensao": 10.0, "tipo_trecho": "Eixo Principal",
         "administracao": "Estadual", "jurisdicao": "Estadual"},
    ])
    a = snv.ancorar(101, "RN", 50.0, coincidentes)
    assert a.houve_desempate is True
    # o federal vence apesar de o estadual ser mais curto
    assert a.codigo == "101BRN0300"


# --- Requisito: regime de administracao ---

def test_administracao_federal_e_dnit():
    assert snv.regime("Federal") == "DNIT"


def test_concessao_federal_e_antt():
    assert snv.regime("Concessão Federal") == "ANTT"


def test_administracao_estadual_e_outro():
    assert snv.regime("Estadual") == "outro"


# --- Requisito: agregacao do custo por segmento ---

def test_agrega_custo_por_segmento_e_por_km():
    ancoragens = pd.DataFrame([
        {"id": "1", "codigo": "101BRN0020"},
        {"id": "2", "codigo": "101BRN0020"},
    ])
    custos = pd.DataFrame([{"id": "1", "total": 100_000.0}, {"id": "2", "total": 300_000.0}])
    r = snv.agregar_por_segmento(ancoragens, custos, segmentos_rn())
    linha = r[r["codigo"] == "101BRN0020"].iloc[0]
    assert linha["custo_social"] == pytest.approx(400_000.0)
    assert linha["custo_por_km"] == pytest.approx(400_000.0 / 14.3)


def test_segmento_em_duas_safras_usa_extensao_da_mais_recente():
    """Repetir o segmento por safra somaria a mesma extensao fisica varias vezes."""
    segs = pd.DataFrame([
        {"safra": "202310A", "br": 101, "uf": "RN", "codigo": "101BRN0020",
         "km_inicial": 6.1, "km_final": 16.1, "extensao": 10.0,
         "tipo_trecho": "Eixo Principal", "administracao": "Federal",
         "jurisdicao": "Federal", "regime": "DNIT"},
        {"safra": "202511A", "br": 101, "uf": "RN", "codigo": "101BRN0020",
         "km_inicial": 6.1, "km_final": 18.1, "extensao": 12.0,
         "tipo_trecho": "Eixo Principal", "administracao": "Federal",
         "jurisdicao": "Federal", "regime": "DNIT"},
    ])
    ancoragens = pd.DataFrame([
        {"id": "1", "codigo": "101BRN0020", "safra": "202310A"},
        {"id": "2", "codigo": "101BRN0020", "safra": "202511A"},
    ])
    custos = pd.DataFrame([{"id": "1", "total": 100_000.0}, {"id": "2", "total": 300_000.0}])
    r = snv.agregar_por_segmento(ancoragens, custos, segs)
    assert len(r) == 1                                    # uma linha, nao duas
    linha = r.iloc[0]
    assert linha["extensao"] == pytest.approx(12.0)       # a da safra mais recente
    assert linha["custo_social"] == pytest.approx(400_000.0)
    assert linha["custo_por_km"] == pytest.approx(400_000.0 / 12.0)
