"""Consulta web somente leitura para o banco consolidado."""
from __future__ import annotations

import json
import sqlite3
from urllib.parse import parse_qs


MAX_PAGE_SIZE = 100


def _identificador_sql(nome: str) -> str:
    return '"' + nome.replace('"', '""') + '"'


def _linhas(cursor: sqlite3.Cursor) -> list[dict]:
    nomes = [coluna[0] for coluna in cursor.description or []]
    return [dict(zip(nomes, linha)) for linha in cursor.fetchall()]


def _json_bytes(valor: dict, status: str = "200 OK") -> tuple[str, bytes]:
    return status, json.dumps(valor, ensure_ascii=False).encode("utf-8")


def _paginacao(parametros: dict[str, list[str]]) -> tuple[int, int]:
    try:
        pagina = int(parametros.get("page", ["1"])[0])
        tamanho = int(parametros.get("page_size", ["20"])[0])
    except ValueError as erro:
        raise ValueError("page e page_size devem ser inteiros") from erro
    if pagina < 1 or tamanho < 1 or tamanho > MAX_PAGE_SIZE:
        raise ValueError(f"page deve ser >= 1 e page_size deve estar entre 1 e {MAX_PAGE_SIZE}")
    return pagina, tamanho


def _resposta_json(start_response, status: str, valor: dict):
    status, corpo = _json_bytes(valor, status)
    start_response(
        status,
        [("Content-Type", "application/json; charset=utf-8"), ("Content-Length", str(len(corpo)))],
    )
    return [corpo]


def _resposta_html(start_response):
    corpo = """<!doctype html>
<html lang="pt-BR">
<head><meta charset="utf-8"><title>Consulta de dados</title></head>
<body>
<h1>Consulta de dados consolidados</h1>
<form id="filtros">
<label>Órgão <input name="fonte"></label>
<label>Data inicial <input name="data_inicio"></label>
<label>Data final <input name="data_fim"></label>
<button type="submit">Consultar</button>
</form>
<p id="mensagem"></p>
<table id="resultados"><thead></thead><tbody></tbody></table>
<script>
const formulario = document.querySelector('#filtros');
const mensagem = document.querySelector('#mensagem');
const tabela = document.querySelector('#resultados');
const escapar = (valor) => String(valor ?? '').replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
formulario.addEventListener('submit', async (evento) => {
  evento.preventDefault();
  const parametros = new URLSearchParams(new FormData(formulario));
  const resposta = await fetch('/api/registros?' + parametros);
  const dados = await resposta.json();
  if (!resposta.ok) { mensagem.textContent = dados.error; return; }
  mensagem.textContent = dados.total ? `${dados.total} registro(s)` : 'Não há resultados.';
  const linhas = dados.items || [];
  const colunas = linhas.length ? Object.keys(linhas[0]) : [];
    tabela.querySelector('thead').innerHTML = '<tr>' + colunas.map((coluna) => `<th>${escapar(coluna)}</th>`).join('') + '</tr>';
    tabela.querySelector('tbody').innerHTML = linhas.map((linha) => '<tr>' + colunas.map((coluna) => `<td>${escapar(linha[coluna])}</td>`).join('') + '</tr>').join('');
});
</script>
</body>
</html>""".encode("utf-8")
    start_response(
        "200 OK",
        [("Content-Type", "text/html; charset=utf-8"), ("Content-Length", str(len(corpo)))],
    )
    return [corpo]


def criar_aplicacao(con: sqlite3.Connection):
    """Cria uma aplicação WSGI de consulta somente leitura."""
    def aplicacao(environ, start_response):
        metodo = environ.get("REQUEST_METHOD", "GET").upper()
        caminho = environ.get("PATH_INFO", "/")
        parametros = parse_qs(environ.get("QUERY_STRING", ""), keep_blank_values=True)

        if metodo != "GET":
            return _resposta_json(start_response, "405 Method Not Allowed", {"error": "somente GET e permitido"})
        if "sql" in parametros:
            return _resposta_json(start_response, "400 Bad Request", {"error": "SQL arbitrario nao e permitido"})
        if caminho == "/":
            return _resposta_html(start_response)

        try:
            pagina, tamanho = _paginacao(parametros)
        except ValueError as erro:
            return _resposta_json(start_response, "400 Bad Request", {"error": str(erro)})
        deslocamento = (pagina - 1) * tamanho

        if caminho == "/api/fontes":
            cursor = con.execute("SELECT fonte FROM fontes ORDER BY fonte")
            return _resposta_json(start_response, "200 OK", {"items": _linhas(cursor)})

        if caminho == "/api/lotes":
            filtros = []
            valores = []
            fonte = parametros.get("fonte", [""])[0]
            if fonte:
                filtros.append("fonte = ?")
                valores.append(fonte)
            where = " WHERE " + " AND ".join(filtros) if filtros else ""
            total = con.execute(f"SELECT COUNT(*) FROM lotes{where}", valores).fetchone()[0]
            cursor = con.execute(
                f"SELECT * FROM lotes{where} ORDER BY lote_id DESC LIMIT ? OFFSET ?",
                valores + [tamanho, deslocamento],
            )
            return _resposta_json(
                start_response,
                "200 OK",
                {"items": _linhas(cursor), "page": pagina, "page_size": tamanho, "total": total},
            )

        if caminho == "/api/registros":
            colunas = [linha[1] for linha in con.execute("PRAGMA table_info(registros_canonicos)")]
            filtros = []
            valores = []
            fonte = parametros.get("fonte", [""])[0]
            if fonte:
                filtros.append("l.fonte = ?")
                valores.append(fonte)
            data_inicio = parametros.get("data_inicio", [""])[0]
            data_fim = parametros.get("data_fim", [""])[0]
            if data_inicio or data_fim:
                if "periodo" not in colunas:
                    return _resposta_json(start_response, "400 Bad Request", {"error": "coluna periodo nao esta disponivel"})
                if data_inicio:
                    filtros.append('r."periodo" >= ?')
                    valores.append(data_inicio)
                if data_fim:
                    filtros.append('r."periodo" <= ?')
                    valores.append(data_fim)
            where = " WHERE " + " AND ".join(filtros) if filtros else ""
            permitidas = {"registro_id", "linha_origem", "fonte", "versao", *colunas}
            ordenacao = parametros.get("order_by", ["registro_id"])[0]
            if ordenacao not in permitidas:
                return _resposta_json(start_response, "400 Bad Request", {"error": "ordenacao nao permitida"})
            direcao = parametros.get("order_dir", ["asc"])[0].lower()
            if direcao not in {"asc", "desc"}:
                return _resposta_json(start_response, "400 Bad Request", {"error": "direcao nao permitida"})
            coluna_ordem = f"l.{_identificador_sql(ordenacao)}" if ordenacao in {"fonte", "versao"} else f"r.{_identificador_sql(ordenacao)}"
            total = con.execute(
                f"SELECT COUNT(*) FROM registros_canonicos r JOIN lotes l ON l.lote_id = r.lote_id{where}",
                valores,
            ).fetchone()[0]
            cursor = con.execute(
                f"SELECT r.*, l.fonte AS origem_fonte, l.arquivo AS origem_arquivo, l.versao AS origem_versao, l.checksum AS origem_checksum "
                f"FROM registros_canonicos r JOIN lotes l ON l.lote_id = r.lote_id{where} "
                f"ORDER BY {coluna_ordem} {direcao} LIMIT ? OFFSET ?",
                valores + [tamanho, deslocamento],
            )
            return _resposta_json(
                start_response,
                "200 OK",
                {"items": _linhas(cursor), "page": pagina, "page_size": tamanho, "total": total},
            )

        if caminho.startswith("/api/registros/"):
            try:
                registro_id = int(caminho.rsplit("/", 1)[1])
            except ValueError:
                return _resposta_json(start_response, "404 Not Found", {"error": "registro nao encontrado"})
            cursor = con.execute(
                "SELECT r.*, l.fonte AS origem_fonte, l.arquivo AS origem_arquivo, "
                "l.versao AS origem_versao, l.checksum AS origem_checksum, l.lote_id AS origem_lote "
                "FROM registros_canonicos r JOIN lotes l ON l.lote_id = r.lote_id "
                "WHERE r.registro_id = ?",
                (registro_id,),
            )
            item = _linhas(cursor)
            if not item:
                return _resposta_json(start_response, "404 Not Found", {"error": "registro nao encontrado"})
            return _resposta_json(start_response, "200 OK", item[0])

        return _resposta_json(start_response, "404 Not Found", {"error": "rota nao encontrada"})

    return aplicacao


def executar_servidor(
    con: sqlite3.Connection,
    host: str = "127.0.0.1",
    port: int = 8000,
):
    """Cria um servidor WSGI local para a aplicacao de consulta."""
    from wsgiref.simple_server import make_server

    return make_server(host, port, criar_aplicacao(con))
