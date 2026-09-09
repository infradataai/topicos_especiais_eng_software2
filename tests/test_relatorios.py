import json
import sqlite3

import pytest

from src.relatorios import RelatorioInvalido, gerar_json, gerar_pdf


@pytest.fixture
def relatorio():
    return {
        "titulo": "Relatorio mensal",
        "periodo": "2026-01",
        "resultados": [{"valor": 10}],
        "metricas": {"media": 10, "mediana": 10},
        "alertas": ["nenhum"],
        "qualidade": {"ok": True},
        "proveniencia": {
            "fonte": "orgao-a",
            "lote": 7,
            "versao": "v1",
            "arquivo": "dados.csv",
        },
    }


def test_gera_json_deterministico_com_proveniencia(relatorio):
    primeiro = gerar_json(relatorio)
    segundo = gerar_json(relatorio)

    documento = json.loads(primeiro)
    assert primeiro == segundo
    assert documento["metricas"]["media"] == 10
    assert documento["proveniencia"]["fonte"] == "orgao-a"
    assert documento["proveniencia"]["lote"] == 7


def test_gera_json_valido_para_resultado_vazio(relatorio):
    relatorio["resultados"] = []

    documento = json.loads(gerar_json(relatorio))

    assert documento["resultados"] == []


def test_gera_pdf_com_secoes_essenciais(relatorio, tmp_path):
    destino = tmp_path / "relatorio.pdf"

    gerado = gerar_pdf(relatorio, destino)

    conteudo = gerado.read_bytes()
    assert gerado == destino
    assert conteudo.startswith(b"%PDF-1.4")
    for secao in (b"Resumo", b"Qualidade", b"Analise", b"Proveniencia", b"Alertas"):
        assert secao in conteudo


def test_rejeita_relatorio_invalido_sem_escrever_pdf(tmp_path):
    destino = tmp_path / "invalido.pdf"

    with pytest.raises(RelatorioInvalido):
        gerar_json({"metricas": {}})
    with pytest.raises(RelatorioInvalido):
        gerar_pdf({"metricas": {}}, destino)

    assert not destino.exists()


def test_exportacao_nao_altera_banco(relatorio, tmp_path):
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE dados (valor INTEGER)")
    con.execute("INSERT INTO dados VALUES (10)")
    antes = con.execute("SELECT COUNT(*) FROM dados").fetchone()[0]

    gerar_json(relatorio)
    gerar_pdf(relatorio, tmp_path / "relatorio.pdf")

    depois = con.execute("SELECT COUNT(*) FROM dados").fetchone()[0]
    assert depois == antes
