"""Consulta web somente leitura para o banco consolidado."""
from __future__ import annotations

import json
import sqlite3
from urllib.parse import parse_qs

from custo_social_core import consultas


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


def _resposta_mapa(start_response):
    """Pagina do mapa dos trechos criticos, nas duas leituras de criticidade.

    A camada base vem da rede publica. Sem rede, o mapa nao desenha e a pagina
    avisa, mantendo a tabela de segmentos utilizavel.
    """
    corpo = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Trechos criticos</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<style>
 body{font-family:system-ui,sans-serif;margin:0;padding:1rem;color:#1a1a1a}
 h1{font-size:1.25rem;margin:0 0 .25rem}
 p.sub{margin:0 0 1rem;color:#555}
 #mapa{height:60vh;min-height:320px;border:1px solid #ccc;border-radius:4px}
 .barra{display:flex;gap:1rem;flex-wrap:wrap;align-items:end;margin:1rem 0}
 label{display:flex;flex-direction:column;font-size:.8rem;color:#444}
 select,input{padding:.35rem;font-size:.9rem}
 table{border-collapse:collapse;width:100%;font-size:.85rem;margin-top:1rem}
 th,td{border-bottom:1px solid #ddd;padding:.4rem .5rem;text-align:right}
 th:first-child,td:first-child,th:nth-child(2),td:nth-child(2){text-align:left}
 thead th{background:#f2f2f2;position:sticky;top:0}
 .aviso{background:#fff4e5;border:1px solid #f0c390;padding:.5rem;border-radius:4px}
 .nulo{color:#999}
</style>
</head>
<body>
<h1>Trechos criticos da malha federal</h1>
<p class="sub">Custo social dos sinistros, a precos de junho de 2026. As duas leituras
de criticidade divergem: por quilometro pesa o trecho movimentado; por
veiculo-quilometro pesa o trecho vazio.</p>

<div class="barra">
 <label>Unidade da federacao <input id="uf" value="RN" size="4"></label>
 <label>Leitura
  <select id="ordem">
   <option value="custo_por_km">custo por quilometro</option>
   <option value="custo_por_veiculo_km">custo por veiculo-quilometro</option>
   <option value="custo_social">custo social total</option>
   <option value="ocorrencias">numero de ocorrencias</option>
  </select>
 </label>
 <label>BR (opcional) <input id="br" size="5"></label>
 <button id="consultar">Consultar</button>
</div>

<div id="alerta"></div>
<div id="mapa"></div>
<p id="mensagem"></p>
<table id="segmentos"><thead></thead><tbody></tbody></table>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const $ = (s) => document.querySelector(s);
const escapar = (v) => String(v ?? '').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const moeda = (v) => v == null ? null : v.toLocaleString('pt-BR',{style:'currency',currency:'BRL',maximumFractionDigits:0});
const COLUNAS = [
  ['codigo','segmento'],['br','BR'],['extensao','extensao (km)'],
  ['ocorrencias','ocorrencias'],['custo_social','custo social'],
  ['vmda','VMDa'],['custo_por_km','R$/km'],['custo_por_veiculo_km','R$/veic-km']
];

let mapa = null, camada = null;
if (window.L) {
  mapa = L.map('mapa').setView([-5.8, -36.0], 7);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {maxZoom: 18, attribution: '&copy; OpenStreetMap'}).addTo(mapa);
  camada = L.layerGroup().addTo(mapa);
} else {
  $('#alerta').innerHTML = '<p class="aviso">A biblioteca do mapa nao carregou. ' +
    'A tabela de segmentos continua disponivel.</p>';
}

const cor = (categoria) => ({obito:'#b00020', ferido_grave:'#e07800',
  ferido_leve:'#0a7d3f', sem_vitimas:'#4a6fa5'}[categoria] || '#666');

async function consultar() {
  const uf = $('#uf').value.trim().toUpperCase();
  const br = $('#br').value.trim();
  const ordem = $('#ordem').value;
  if (!uf) { $('#mensagem').textContent = 'Informe a unidade da federacao.'; return; }

  const p = new URLSearchParams({uf, order_by: ordem, order_dir: 'desc', page_size: '50'});
  const resposta = await fetch('/api/segmentos?' + p);
  const dados = await resposta.json();
  if (!resposta.ok) { $('#mensagem').textContent = dados.error; return; }
  $('#mensagem').textContent = dados.total
    ? dados.total + ' segmento(s) com ocorrencia ancorada'
    : 'Nao ha segmentos para esta unidade da federacao.';

  const tabela = $('#segmentos');
  tabela.querySelector('thead').innerHTML = '<tr>' +
    COLUNAS.map(([,r]) => '<th>' + escapar(r) + '</th>').join('') + '</tr>';
  tabela.querySelector('tbody').innerHTML = (dados.items || []).map((linha) => '<tr>' +
    COLUNAS.map(([c]) => {
      let v = linha[c];
      if (v == null) return '<td class="nulo">sem medicao</td>';
      if (c === 'custo_social' || c === 'custo_por_km') v = moeda(v);
      else if (c === 'custo_por_veiculo_km') v = v.toLocaleString('pt-BR',{maximumFractionDigits:4});
      else if (typeof v === 'number') v = v.toLocaleString('pt-BR',{maximumFractionDigits:1});
      return '<td>' + escapar(v) + '</td>';
    }).join('') + '</tr>').join('');

  if (!camada) return;
  const q = new URLSearchParams({uf, page_size: '100'});
  if (br) q.set('br', br);
  const rOcor = await fetch('/api/ocorrencias?' + q);
  const ocor = await rOcor.json();
  if (!rOcor.ok) return;
  camada.clearLayers();
  const pontos = [];
  for (const o of ocor.items || []) {
    if (o.latitude == null || o.longitude == null) continue;
    pontos.push([o.latitude, o.longitude]);
    L.circleMarker([o.latitude, o.longitude], {
      radius: 4 + Math.log10(Math.max(o.custo_social || 1, 1)),
      color: cor(o.categoria), fillOpacity: .6, weight: 1
    }).bindPopup('BR-' + escapar(o.br) + ' km ' + escapar(o.km) + '<br>' +
      escapar(o.ano) + ' &middot; ' + escapar(o.categoria) + '<br>' +
      escapar(moeda(o.custo_social))).addTo(camada);
  }
  if (pontos.length) mapa.fitBounds(pontos, {padding: [20, 20]});
}

$('#consultar').addEventListener('click', consultar);
consultar();
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
        if caminho == "/mapa":
            return _resposta_mapa(start_response)

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

        # --- esquema de sinistros (nucleo do projeto final) -------------------
        if caminho in {"/api/segmentos", "/api/ocorrencias", "/api/resumo"}:
            if not consultas.tem_esquema_de_sinistros(con):
                return _resposta_json(
                    start_response, "400 Bad Request",
                    {"error": "este banco nao tem as tabelas de sinistro"})
            uf = parametros.get("uf", [""])[0].strip().upper()
            if not uf:
                return _resposta_json(
                    start_response, "400 Bad Request",
                    {"error": "informe a unidade da federacao em uf"})
            try:
                br = int(parametros["br"][0]) if parametros.get("br", [""])[0] else None
                ano = int(parametros["ano"][0]) if parametros.get("ano", [""])[0] else None
            except ValueError:
                return _resposta_json(
                    start_response, "400 Bad Request",
                    {"error": "br e ano devem ser inteiros"})
            direcao = parametros.get("order_dir", ["desc"])[0]

            if caminho == "/api/resumo":
                return _resposta_json(start_response, "200 OK", consultas.resumo(con, uf))

            try:
                if caminho == "/api/segmentos":
                    itens = consultas.segmentos_criticos(
                        con, uf,
                        ordenar_por=parametros.get("order_by", ["custo_por_km"])[0],
                        direcao=direcao, limite=tamanho, deslocamento=deslocamento)
                    total = consultas.contar_segmentos(con, uf)
                else:
                    itens = consultas.ocorrencias(
                        con, uf, br=br, ano=ano,
                        ordenar_por=parametros.get("order_by", ["id"])[0],
                        direcao=parametros.get("order_dir", ["asc"])[0],
                        limite=tamanho, deslocamento=deslocamento)
                    total = consultas.contar_ocorrencias(con, uf, br=br, ano=ano)
            except ValueError as erro:
                return _resposta_json(start_response, "400 Bad Request", {"error": str(erro)})
            return _resposta_json(
                start_response, "200 OK",
                {"items": itens, "page": pagina, "page_size": tamanho, "total": total})

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
