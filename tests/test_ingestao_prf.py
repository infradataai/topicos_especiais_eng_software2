"""Testes da ingestao e deduplicacao da PRF (RF01 a RF04)."""
from __future__ import annotations

import pandas as pd
import pytest

from custo_social_core import ingestao_prf


def bruto_exemplo() -> pd.DataFrame:
    """Duas pessoas de um acidente, cada uma repetida em duas causas/tipos.

    Reproduz a repeticao do conjunto "todas as causas e tipos": quatro linhas
    para duas pessoas e dois veiculos.
    """
    linhas = []
    for causa, tipo in [("Velocidade incompativel", "Colisao frontal"),
                        ("Ingestao de alcool", "Saida de leito carrocavel")]:
        linhas += [
            {"id": "1", "pesid": "10", "id_veiculo": "100", "uf": "RN", "br": "101",
             "km": "12,5", "data_inversa": "2022-03-15", "estado_fisico": "Óbito",
             "tipo_envolvido": "Condutor", "idade": "34", "sexo": "Masculino",
             "tipo_veiculo": "Motocicleta", "classificacao_acidente": "Com Vítimas Fatais",
             "ilesos": "0", "feridos_leves": "0", "feridos_graves": "0", "mortos": "1",
             "causa_principal": "Sim", "causa_acidente": causa,
             "ordem_tipo_acidente": "1", "tipo_acidente": tipo},
            {"id": "1", "pesid": "11", "id_veiculo": "101", "uf": "RN", "br": "101",
             "km": "12,5", "data_inversa": "2022-03-15", "estado_fisico": "Lesões Leves",
             "tipo_envolvido": "Condutor", "idade": "50", "sexo": "Feminino",
             "tipo_veiculo": "Automóvel", "classificacao_acidente": "Com Vítimas Fatais",
             "ilesos": "0", "feridos_leves": "1", "feridos_graves": "0", "mortos": "0",
             "causa_principal": "Não", "causa_acidente": causa,
             "ordem_tipo_acidente": "1", "tipo_acidente": tipo},
        ]
    return pd.DataFrame(linhas)


# --- deduplicacao ---

def test_deduplica_pessoas_e_veiculos_sem_perder_causas():
    t = ingestao_prf.normalizar(bruto_exemplo())
    assert len(t["ocorrencias"]) == 1      # um acidente
    assert len(t["pessoas"]) == 2          # duas pessoas, nao quatro linhas
    assert len(t["veiculos"]) == 2         # dois veiculos
    assert len(t["causas_tipos"]) == 2     # as duas causas preservadas


def test_preserva_causas_e_tipos_no_grao_proprio():
    # A causa e o tipo saem da tabela de pessoas e vao para a tabela propria,
    # sem descarte: e o que permite deduplicar sem perder informacao.
    t = ingestao_prf.normalizar(bruto_exemplo())
    causas = set(t["causas_tipos"]["causa_acidente"])
    assert causas == {"Velocidade incompativel", "Ingestao de alcool"}
    assert "causa_acidente" not in t["pessoas"].columns


def test_le_apenas_as_linhas_da_uf_pedida(tmp_path):
    f = tmp_path / "acidentes2019_todas_causas_tipos.csv"
    cabecalho = "id;pesid;id_veiculo;uf;estado_fisico"
    f.write_text(
        f"{cabecalho}\n1;10;100;RN;Ileso\n2;20;200;PB;Ileso\n3;30;300;RN;Óbito\n",
        encoding="latin-1",
    )
    bruto = ingestao_prf.ler_ano(f, "RN")
    assert len(bruto) == 2
    assert set(bruto["uf"]) == {"RN"}


def test_gravidade_mapeada_a_partir_do_estado_fisico():
    t = ingestao_prf.normalizar(bruto_exemplo())
    assert set(t["pessoas"]["gravidade"]) == {"obito", "ferido_leve"}


def test_nao_informado_vira_categoria_e_nao_nulo():
    b = bruto_exemplo()
    b.loc[b["pesid"] == "11", "estado_fisico"] = "Não Informado"
    t = ingestao_prf.normalizar(b)
    assert "nao_informado" in set(t["pessoas"]["gravidade"])
    assert t["pessoas"]["gravidade"].notna().all()


# --- parsing de data (o defeito real encontrado no arquivo de 2022) ---

def test_data_iso_e_brasileira_no_mesmo_pipeline():
    s = pd.Series(["2019-01-01", "01/01/2022", "25/12/2022", "2024-07-09"])
    d = ingestao_prf.parse_data(s)
    assert list(d.dt.year) == [2019, 2022, 2022, 2024]
    assert list(d.dt.month) == [1, 1, 12, 7]


def test_dia_maior_que_doze_no_formato_brasileiro_nao_vira_nulo():
    # Era exatamente aqui que a inferencia automatica descartava a linha.
    d = ingestao_prf.parse_data(pd.Series(["31/03/2022"]))
    assert d.notna().all()
    assert d.dt.month.iloc[0] == 3 and d.dt.day.iloc[0] == 31


def test_texto_fora_de_formato_conhecido_vira_nulo_declarado():
    d = ingestao_prf.parse_data(pd.Series(["sem data", ""]))
    assert d.isna().all()


# --- validacao cruzada ---

def test_validacao_confirma_contagem_por_gravidade():
    t = ingestao_prf.normalizar(bruto_exemplo())
    achados = {a["verificacao"]: a for a in ingestao_prf.validar(t)}
    obito = achados["pessoas com gravidade 'obito' x soma do indicador 'mortos'"]
    assert obito["situacao"] == "ok" and obito["obtido"] == 1


def test_validacao_acusa_chave_duplicada():
    t = ingestao_prf.normalizar(bruto_exemplo())
    t["pessoas"] = pd.concat([t["pessoas"], t["pessoas"].head(1)], ignore_index=True)
    achados = {a["verificacao"]: a for a in ingestao_prf.validar(t)}
    assert achados["chave (id, pesid) unica"]["situacao"] == "divergencia"


# --- vetor C do modelo aditivo do IPEA ---

def test_vetor_c_conta_pessoas_e_veiculos_por_ocorrencia():
    t = ingestao_prf.normalizar(bruto_exemplo())
    c = ingestao_prf.vetor_c(t)
    linha = c.iloc[0]
    assert linha["obito"] == 1
    assert linha["ferido_leve"] == 1
    assert linha["veic_Motocicleta"] == 1
    assert linha["veic_Automóvel"] == 1


def test_arquivo_sem_pesid_falha_em_vez_de_deduplicar_por_aproximacao(tmp_path):
    f = tmp_path / "acidentes2019_todas_causas_tipos.csv"
    f.write_text("id;uf;estado_fisico\n1;RN;Ileso\n", encoding="latin-1")
    with pytest.raises(ingestao_prf.ColunaObrigatoriaAusente):
        ingestao_prf.ler_ano(f, "RN")
