"""Testes da consolidacao em SQLite: esquema, idempotencia e proveniencia.

Cada teste corresponde a um cenario de
openspec/changes/consolidacao-e-snv/specs/persistencia/spec.md.
Escritos ANTES da implementacao.
"""
from __future__ import annotations

import pandas as pd

from custo_social_core import persistencia as pst

OCORRENCIAS = pd.DataFrame([
    {"id": "1", "uf": "RN", "br": 101, "km": 12.5, "ano": 2024,
     "classificacao_acidente": "Com Vítimas Feridas"},
    {"id": "2", "uf": "RN", "br": 304, "km": 40.0, "ano": 2024,
     "classificacao_acidente": "Sem Vítimas"},
])


# --- Requisito: esquema relacional unico ---

def test_cria_esquema_em_banco_novo(tmp_path):
    eng = pst.criar_esquema(tmp_path / "novo.db")
    for t in ("ocorrencias", "veiculos", "pessoas", "segmentos_snv",
              "custo_ocorrencia", "ancoragem", "proveniencia"):
        assert pst.contar(eng, t) == 0


# --- Requisito: carga idempotente ---

def test_recarregar_mesma_origem_nao_duplica(tmp_path):
    eng = pst.criar_esquema(tmp_path / "b.db")
    pst.carregar(eng, "ocorrencias", OCORRENCIAS, orgao="PRF",
                 arquivo="acidentes2024.csv", referencia="2024")
    pst.carregar(eng, "ocorrencias", OCORRENCIAS, orgao="PRF",
                 arquivo="acidentes2024.csv", referencia="2024")
    assert pst.contar(eng, "ocorrencias") == 2


def test_carga_parcial_insere_so_o_inedito(tmp_path):
    eng = pst.criar_esquema(tmp_path / "b.db")
    pst.carregar(eng, "ocorrencias", OCORRENCIAS, orgao="PRF",
                 arquivo="a.csv", referencia="2024")
    novo = pd.concat([OCORRENCIAS.head(1), pd.DataFrame([
        {"id": "3", "uf": "RN", "br": 226, "km": 5.0, "ano": 2025,
         "classificacao_acidente": "Com Vítimas Fatais"}])], ignore_index=True)
    inseridas = pst.carregar(eng, "ocorrencias", novo, orgao="PRF",
                             arquivo="b.csv", referencia="2025")
    assert inseridas == 1
    assert pst.contar(eng, "ocorrencias") == 3


# --- Requisito: rastreamento de origem e versao ---

def test_proveniencia_registra_orgao_arquivo_e_ano(tmp_path):
    eng = pst.criar_esquema(tmp_path / "b.db")
    pst.carregar(eng, "ocorrencias", OCORRENCIAS, orgao="PRF",
                 arquivo="acidentes2024.csv", referencia="2024")
    p = pst.proveniencia(eng, "ocorrencias")
    assert len(p) == 1
    r = p.iloc[0]
    assert r["orgao"] == "PRF"
    assert r["arquivo"] == "acidentes2024.csv"
    assert r["referencia"] == "2024"
    assert pd.notna(r["carregado_em"])


def test_duas_origens_na_mesma_tabela(tmp_path):
    eng = pst.criar_esquema(tmp_path / "b.db")
    pst.carregar(eng, "ocorrencias", OCORRENCIAS.head(1), orgao="PRF",
                 arquivo="a2024.csv", referencia="2024")
    pst.carregar(eng, "ocorrencias", OCORRENCIAS.tail(1), orgao="PRF",
                 arquivo="a2025.csv", referencia="2025")
    p = pst.proveniencia(eng, "ocorrencias")
    assert len(p) == 2
    assert set(p["referencia"]) == {"2024", "2025"}


# --- Requisito: consulta por unidade da federacao ---

def test_consulta_custo_por_segmento_de_uma_uf(tmp_path):
    eng = pst.criar_esquema(tmp_path / "b.db")
    oc = pd.concat([OCORRENCIAS, pd.DataFrame([
        {"id": "9", "uf": "PB", "br": 101, "km": 3.0, "ano": 2024,
         "classificacao_acidente": "Sem Vítimas"}])], ignore_index=True)
    pst.carregar(eng, "ocorrencias", oc, orgao="PRF", arquivo="a.csv", referencia="2024")
    pst.carregar(eng, "segmentos_snv", pd.DataFrame([
        {"safra": "202501A", "codigo": "101BRN0020", "br": 101, "uf": "RN",
         "km_inicial": 6.1, "km_final": 20.4, "extensao": 14.3,
         "administracao": "Federal", "jurisdicao": "Federal",
         "tipo_trecho": "Eixo Principal", "regime": "DNIT"},
        {"safra": "202501A", "codigo": "101BPB0010", "br": 101, "uf": "PB",
         "km_inicial": 0.0, "km_final": 10.0, "extensao": 10.0,
         "administracao": "Federal", "jurisdicao": "Federal",
         "tipo_trecho": "Eixo Principal", "regime": "DNIT"}]),
        orgao="DNIT", arquivo="SNV_202501A.xls", referencia="202501A")
    pst.carregar(eng, "custo_ocorrencia", pd.DataFrame([
        {"id": "1", "total": 100_000.0, "categoria": "com_vitima_leve"},
        {"id": "9", "total": 50_000.0, "categoria": "sem_vitimas"}]),
        orgao="interno", arquivo="calculo", referencia="jun/2026")
    pst.carregar(eng, "ancoragem", pd.DataFrame([
        {"id": "1", "safra": "202501A", "codigo_segmento": "101BRN0020",
         "houve_desempate": 0, "motivo": ""},
        {"id": "9", "safra": "202501A", "codigo_segmento": "101BPB0010",
         "houve_desempate": 0, "motivo": ""}]),
        orgao="interno", arquivo="ancoragem", referencia="202501A")

    r = pst.custo_por_segmento(eng, uf="RN")
    assert len(r) == 1
    assert r.iloc[0]["codigo"] == "101BRN0020"
    assert r.iloc[0]["custo_social"] == 100_000.0


def test_segmento_em_varias_safras_nao_duplica_o_custo(tmp_path):
    """O mesmo codigo existe em toda safra; juntar so por codigo multiplicaria o custo."""
    eng = pst.criar_esquema(tmp_path / "b.db")
    pst.carregar(eng, "ocorrencias", OCORRENCIAS.head(1), orgao="PRF",
                 arquivo="a.csv", referencia="2024")
    base = {"codigo": "101BRN0020", "br": 101, "uf": "RN", "km_inicial": 6.1,
            "km_final": 20.4, "extensao": 14.3, "administracao": "Federal",
            "jurisdicao": "Federal", "tipo_trecho": "Eixo Principal", "regime": "DNIT"}
    # o mesmo segmento em tres safras
    pst.carregar(eng, "segmentos_snv", pd.DataFrame(
        [{**base, "safra": s} for s in ("202310A", "202410A", "202511A")]),
        orgao="DNIT", arquivo="SNV", referencia="varias")
    pst.carregar(eng, "custo_ocorrencia", pd.DataFrame(
        [{"id": "1", "total": 100_000.0, "categoria": "com_vitima_leve"}]),
        orgao="interno", arquivo="calculo", referencia="jun/2026")
    pst.carregar(eng, "ancoragem", pd.DataFrame(
        [{"id": "1", "safra": "202410A", "codigo_segmento": "101BRN0020",
          "houve_desempate": 0, "motivo": ""}]),
        orgao="interno", arquivo="ancoragem", referencia="202410A")

    r = pst.custo_por_segmento(eng, uf="RN")
    assert len(r) == 1
    assert r.iloc[0]["custo_social"] == 100_000.0    # e nao 300.000
    assert r.iloc[0]["ocorrencias"] == 1


def test_segmento_ancorado_em_duas_safras_usa_extensao_da_mais_recente(tmp_path):
    """Uma linha por segmento; extensao da safra mais recente, custo de todas."""
    eng = pst.criar_esquema(tmp_path / "b.db")
    pst.carregar(eng, "ocorrencias", OCORRENCIAS, orgao="PRF",
                 arquivo="a.csv", referencia="2024")
    base = {"codigo": "101BRN0020", "br": 101, "uf": "RN", "km_inicial": 6.1,
            "administracao": "Federal", "jurisdicao": "Federal",
            "tipo_trecho": "Eixo Principal", "regime": "DNIT"}
    pst.carregar(eng, "segmentos_snv", pd.DataFrame([
        {**base, "safra": "202310A", "km_final": 16.1, "extensao": 10.0},
        {**base, "safra": "202511A", "km_final": 18.1, "extensao": 12.0}]),
        orgao="DNIT", arquivo="SNV", referencia="duas")
    pst.carregar(eng, "custo_ocorrencia", pd.DataFrame([
        {"id": "1", "total": 100_000.0, "categoria": "com_vitima_leve"},
        {"id": "2", "total": 300_000.0, "categoria": "sem_vitimas"}]),
        orgao="interno", arquivo="calculo", referencia="jun/2026")
    pst.carregar(eng, "ancoragem", pd.DataFrame([
        {"id": "1", "safra": "202310A", "codigo_segmento": "101BRN0020",
         "houve_desempate": 0, "motivo": ""},
        {"id": "2", "safra": "202511A", "codigo_segmento": "101BRN0020",
         "houve_desempate": 0, "motivo": ""}]),
        orgao="interno", arquivo="ancoragem", referencia="duas")

    r = pst.custo_por_segmento(eng, uf="RN")
    assert len(r) == 1
    assert r.iloc[0]["extensao"] == 12.0              # a da safra mais recente
    assert r.iloc[0]["custo_social"] == 400_000.0     # soma das duas safras
    assert r.iloc[0]["ocorrencias"] == 2


# --- Requisito: nenhum dado pessoal no banco versionado ---

def test_banco_fica_na_pasta_de_dados():
    p = pst.caminho_banco_padrao()
    assert "dados" in p.parts


# --- robustez de tipos: o SQLite nao vincula Timestamp nem tipos do numpy ---

def test_carrega_data_como_timestamp_do_pandas(tmp_path):
    import numpy as np
    eng = pst.criar_esquema(tmp_path / "b.db")
    df = pd.DataFrame([{"id": "1", "uf": "RN", "br": np.int64(101),
                        "km": np.float64(12.5), "data": pd.Timestamp("2024-03-15"),
                        "ano": np.int64(2024), "mes": np.int64(3),
                        "classificacao_acidente": "Sem Vítimas",
                        "latitude": None, "longitude": float("nan")}])
    pst.carregar(eng, "ocorrencias", df, orgao="PRF", arquivo="a.csv", referencia="2024")
    assert pst.contar(eng, "ocorrencias") == 1
