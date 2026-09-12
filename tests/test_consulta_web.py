import json
import sqlite3
from io import BytesIO
from urllib.parse import urlsplit

from wsgiref.util import setup_testing_defaults

from src.consulta_web import criar_aplicacao


def _banco():
    con = sqlite3.connect(":memory:")
    con.executescript(
        """
        CREATE TABLE fontes (fonte TEXT PRIMARY KEY);
        CREATE TABLE lotes (
            lote_id INTEGER PRIMARY KEY,
            fonte TEXT,
            arquivo TEXT,
            checksum TEXT,
            versao TEXT,
            ingerido_em TEXT,
            configuracao_json TEXT,
            valido INTEGER,
            registros_validos INTEGER,
            registros_invalidos INTEGER,
            idempotente INTEGER
        );
        CREATE TABLE registros_canonicos (
            registro_id INTEGER PRIMARY KEY,
            lote_id INTEGER,
            linha_origem INTEGER,
            fingerprint TEXT,
            periodo TEXT,
            valor TEXT
        );
        INSERT INTO fontes VALUES ('orgao-a'), ('orgao-b');
        INSERT INTO lotes VALUES
            (1, 'orgao-a', 'a.csv', 'abc', 'v1', '2026-01-01', '{}', 1, 1, 0, 0),
            (2, 'orgao-b', 'b.xlsx', 'def', 'v2', '2026-01-02', '{}', 1, 1, 0, 0);
        INSERT INTO registros_canonicos VALUES
            (1, 1, 1, 'hash-a', '2026-01', '10'),
            (2, 2, 1, 'hash-b', '2026-02', '20');
        """
    )
    con.commit()
    return con


def _request(app, url, method="GET"):
    partes = urlsplit(url)
    ambiente = {}
    setup_testing_defaults(ambiente)
    ambiente.update(
        {
            "REQUEST_METHOD": method,
            "PATH_INFO": partes.path,
            "QUERY_STRING": partes.query,
            "wsgi.input": BytesIO(),
        }
    )
    resposta = {}

    def start_response(status, headers):
        resposta["status"] = status
        resposta["headers"] = headers

    corpo = b"".join(app(ambiente, start_response))
    resposta["json"] = json.loads(corpo)
    return resposta


def test_filtra_pagina_e_exibe_proveniencia():
    resposta = _request(
        criar_aplicacao(_banco()),
        "/api/registros?fonte=orgao-a&data_inicio=2026-01&data_fim=2026-01&page_size=1",
    )

    assert resposta["status"] == "200 OK"
    assert resposta["json"]["total"] == 1
    assert resposta["json"]["items"][0]["origem_fonte"] == "orgao-a"
    assert resposta["json"]["items"][0]["origem_checksum"] == "abc"


def test_consulta_fontes_lotes_e_detalhe():
    app = criar_aplicacao(_banco())

    assert _request(app, "/api/fontes")["json"]["items"] == [
        {"fonte": "orgao-a"},
        {"fonte": "orgao-b"},
    ]
    assert _request(app, "/api/lotes?fonte=orgao-b")["json"]["total"] == 1
    detalhe = _request(app, "/api/registros/2")
    assert detalhe["json"]["origem_lote"] == 2
    assert detalhe["json"]["origem_versao"] == "v2"


def test_resultado_vazio_e_paginacao_invalida():
    app = criar_aplicacao(_banco())

    vazio = _request(app, "/api/registros?fonte=inexistente")
    assert vazio["status"] == "200 OK"
    assert vazio["json"]["total"] == 0
    assert vazio["json"]["items"] == []
    assert _request(app, "/api/registros?page_size=101")["status"] == "400 Bad Request"


def test_rejeita_sql_e_escrita():
    con = _banco()
    app = criar_aplicacao(con)
    antes = con.execute("SELECT COUNT(*) FROM registros_canonicos").fetchone()[0]

    sql = _request(app, "/api/registros?sql=DELETE+FROM+registros_canonicos")
    escrita = _request(app, "/api/registros", method="POST")

    assert sql["status"] == "400 Bad Request"
    assert escrita["status"] == "405 Method Not Allowed"
    assert con.execute("SELECT COUNT(*) FROM registros_canonicos").fetchone()[0] == antes
