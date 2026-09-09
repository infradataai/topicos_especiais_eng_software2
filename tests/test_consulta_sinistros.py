"""Testes das consultas do esquema de sinistros e das rotas que as expoem.

Spec em openspec/changes/2026-09-09-mapa-trechos-criticos/specs/consulta/.
"""
from __future__ import annotations

import json
import sqlite3
from io import BytesIO

import pytest

from custo_social_core import consultas
from src.consulta_web import criar_aplicacao


# --- fixtures -------------------------------------------------------------

ESQUEMA = """
CREATE TABLE ocorrencias (
  id TEXT PRIMARY KEY, uf TEXT, br INTEGER, km REAL, data TEXT,
  ano INTEGER, mes INTEGER, classificacao_acidente TEXT,
  latitude REAL, longitude REAL);
CREATE TABLE custo_ocorrencia (
  id TEXT PRIMARY KEY, total REAL, subtotal_pessoas REAL,
  subtotal_veiculos REAL, subtotal_institucional REAL,
  categoria TEXT, base_monetaria TEXT);
CREATE TABLE segmentos_snv (
  safra TEXT, codigo TEXT, br INTEGER, uf TEXT,
  km_inicial REAL, km_final REAL, extensao REAL,
  administracao TEXT, jurisdicao TEXT, tipo_trecho TEXT, regime TEXT,
  PRIMARY KEY (safra, codigo));
CREATE TABLE ancoragem (
  id TEXT PRIMARY KEY, safra TEXT, codigo_segmento TEXT,
  houve_desempate INTEGER, motivo TEXT);
CREATE TABLE exposicao_segmento (
  ano INTEGER, codigo TEXT, br INTEGER, uf TEXT, extensao REAL,
  vmda REAL, n_postos INTEGER, sentidos_completos INTEGER, safra_vmda TEXT,
  PRIMARY KEY (ano, codigo));
"""


@pytest.fixture
def banco() -> sqlite3.Connection:
    """Dois segmentos: um movimentado e curto, outro vazio e longo."""
    con = sqlite3.connect(":memory:")
    con.executescript(ESQUEMA)

    # o segmento 101ABC aparece em duas safras: a agregacao nao pode duplicar o custo
    con.executemany(
        "INSERT INTO segmentos_snv VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        [("202101A", "101ABC", 101, "RN", 0.0, 10.0, 10.0, "Federal", "Federal", "Eixo Principal", "DNIT"),
         ("202301A", "101ABC", 101, "RN", 0.0, 10.0, 10.0, "Federal", "Federal", "Eixo Principal", "DNIT"),
         ("202301A", "304XYZ", 304, "RN", 0.0, 40.0, 40.0, "Federal", "Federal", "Eixo Principal", "DNIT")],
    )
    con.executemany(
        "INSERT INTO ocorrencias VALUES (?,?,?,?,?,?,?,?,?,?)",
        [("o1", "RN", 101, 5.0, "2021-03-01", 2021, 3, "Com Vítimas Fatais", -5.79, -35.21),
         ("o2", "RN", 101, 6.0, "2023-04-01", 2023, 4, "Com Vítimas Feridas", -5.80, -35.22),
         ("o3", "RN", 304, 12.0, "2023-05-01", 2023, 5, "Com Vítimas Fatais", -5.60, -36.10)],
    )
    con.executemany(
        "INSERT INTO custo_ocorrencia VALUES (?,?,?,?,?,?,?)",
        [("o1", 1_000_000.0, 900_000.0, 80_000.0, 20_000.0, "obito", "jun/2026"),
         ("o2", 200_000.0, 150_000.0, 40_000.0, 10_000.0, "ferido_leve", "jun/2026"),
         ("o3", 2_000_000.0, 1_800_000.0, 150_000.0, 50_000.0, "obito", "jun/2026")],
    )
    con.executemany(
        "INSERT INTO ancoragem VALUES (?,?,?,?,?)",
        [("o1", "202101A", "101ABC", 0, ""),
         ("o2", "202301A", "101ABC", 0, ""),
         ("o3", "202301A", "304XYZ", 0, "")],
    )
    # so o 101ABC tem posto de contagem
    con.execute(
        "INSERT INTO exposicao_segmento VALUES (?,?,?,?,?,?,?,?,?)",
        (2023, "101ABC", 101, "RN", 10.0, 20_000.0, 2, 1, "2023"),
    )
    con.commit()
    return con


@pytest.fixture
def banco_lai() -> sqlite3.Connection:
    """Banco com o esquema da LAI, sem as tabelas do nucleo."""
    con = sqlite3.connect(":memory:")
    con.executescript(
        "CREATE TABLE fontes (fonte TEXT PRIMARY KEY);"
        "CREATE TABLE lotes (lote_id INTEGER PRIMARY KEY, fonte TEXT,"
        " arquivo TEXT, versao TEXT, checksum TEXT);"
        "CREATE TABLE registros_canonicos (registro_id INTEGER PRIMARY KEY,"
        " lote_id INTEGER, linha_origem INTEGER);"
    )
    con.commit()
    return con


def chamar(app, caminho: str, consulta: str = ""):
    """Executa a aplicacao WSGI e devolve status e corpo decodificado."""
    capturado = {}

    def start_response(status, cabecalhos):
        capturado["status"] = status
        capturado["cabecalhos"] = dict(cabecalhos)

    corpo = b"".join(app({
        "REQUEST_METHOD": "GET", "PATH_INFO": caminho,
        "QUERY_STRING": consulta, "wsgi.input": BytesIO(b""),
    }, start_response))
    return capturado["status"], capturado["cabecalhos"], corpo


# --- consultas ------------------------------------------------------------

def test_segmentos_traz_as_duas_leituras(banco):
    linhas = consultas.segmentos_criticos(banco, "RN")
    por_codigo = {l["codigo"]: l for l in linhas}
    assert set(por_codigo) == {"101ABC", "304XYZ"}

    movimentado = por_codigo["101ABC"]
    assert movimentado["custo_social"] == pytest.approx(1_200_000.0)
    assert movimentado["custo_por_km"] == pytest.approx(120_000.0)
    # exposicao = 20.000 veic/dia x 10 km x 365 dias = 73.000.000 veiculos-km
    assert movimentado["custo_por_veiculo_km"] == pytest.approx(1_200_000.0 / 73_000_000.0)


def test_nao_multiplica_custo_por_safra(banco):
    """O codigo 101ABC existe em duas safras. Somar as duas dobraria o custo."""
    linhas = consultas.segmentos_criticos(banco, "RN")
    movimentado = next(l for l in linhas if l["codigo"] == "101ABC")
    assert movimentado["ocorrencias"] == 2
    assert movimentado["custo_social"] == pytest.approx(1_200_000.0)
    assert movimentado["extensao"] == pytest.approx(10.0)


def test_segmento_sem_vmda_tem_leitura_por_exposicao_nula(banco):
    linhas = consultas.segmentos_criticos(banco, "RN")
    vazio = next(l for l in linhas if l["codigo"] == "304XYZ")
    assert vazio["vmda"] is None
    assert vazio["custo_por_veiculo_km"] is None
    assert vazio["custo_por_km"] == pytest.approx(50_000.0)


def test_ranques_divergem_entre_as_duas_leituras(banco):
    """O trecho vazio e mais critico por quilometro? Nao. Mas por exposicao, sim."""
    por_km = consultas.segmentos_criticos(banco, "RN", ordenar_por="custo_por_km")
    assert por_km[0]["codigo"] == "101ABC"
    # o 304XYZ nao tem exposicao medida, e por isso nao entra no ranque por exposicao
    por_exposicao = consultas.segmentos_criticos(banco, "RN", ordenar_por="custo_por_veiculo_km")
    assert por_exposicao[0]["codigo"] == "101ABC"


def test_ocorrencias_trazem_coordenada_e_custo(banco):
    linhas = consultas.ocorrencias(banco, "RN", limite=10, deslocamento=0)
    assert len(linhas) == 3
    primeira = linhas[0]
    for campo in ("id", "br", "km", "ano", "latitude", "longitude", "custo_social", "categoria"):
        assert campo in primeira


def test_ocorrencias_filtram_por_br_e_ano(banco):
    linhas = consultas.ocorrencias(banco, "RN", br=101, ano=2023, limite=10, deslocamento=0)
    assert [l["id"] for l in linhas] == ["o2"]
    assert consultas.contar_ocorrencias(banco, "RN", br=101) == 2


def test_esquema_ausente_e_detectado(banco_lai, banco):
    assert consultas.tem_esquema_de_sinistros(banco) is True
    assert consultas.tem_esquema_de_sinistros(banco_lai) is False


def test_ordenacao_fora_da_lista_e_recusada(banco):
    with pytest.raises(ValueError):
        consultas.segmentos_criticos(banco, "RN", ordenar_por="total; DROP TABLE ocorrencias")


# --- rotas ----------------------------------------------------------------

def test_rota_segmentos_responde_ordenada(banco):
    app = criar_aplicacao(banco)
    status, _, corpo = chamar(app, "/api/segmentos", "uf=RN&order_by=custo_por_km&order_dir=desc")
    assert status.startswith("200")
    dados = json.loads(corpo)
    assert dados["total"] == 2
    assert dados["items"][0]["codigo"] == "101ABC"


def test_rota_ocorrencias_traz_coordenada_e_custo(banco):
    app = criar_aplicacao(banco)
    status, _, corpo = chamar(app, "/api/ocorrencias", "uf=RN&br=101")
    assert status.startswith("200")
    dados = json.loads(corpo)
    assert dados["total"] == 2
    assert all(i["latitude"] is not None for i in dados["items"])
    assert all("custo_social" in i for i in dados["items"])


def test_banco_sem_tabelas_de_sinistro_recusa_com_mensagem(banco_lai):
    app = criar_aplicacao(banco_lai)
    status, _, corpo = chamar(app, "/api/segmentos", "uf=RN")
    assert status.startswith("400")
    assert "sinistro" in json.loads(corpo)["error"].lower()


def test_ordenacao_nao_permitida_e_recusada_pela_rota(banco):
    app = criar_aplicacao(banco)
    status, _, corpo = chamar(app, "/api/segmentos", "uf=RN&order_by=drop")
    assert status.startswith("400")


def test_rota_de_sinistros_exige_uf(banco):
    app = criar_aplicacao(banco)
    status, _, _ = chamar(app, "/api/segmentos", "")
    assert status.startswith("400")


def test_pagina_do_mapa_responde_html(banco):
    app = criar_aplicacao(banco)
    status, cabecalhos, corpo = chamar(app, "/mapa")
    assert status.startswith("200")
    assert "text/html" in cabecalhos["Content-Type"]
    pagina = corpo.decode("utf-8")
    assert 'id="mapa"' in pagina
    assert "custo_por_veiculo_km" in pagina


def test_mapa_continua_recusando_sql_do_cliente(banco):
    app = criar_aplicacao(banco)
    status, _, _ = chamar(app, "/api/segmentos", "uf=RN&sql=SELECT+1")
    assert status.startswith("400")
