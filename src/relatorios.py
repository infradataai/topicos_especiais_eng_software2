"""Exportacao deterministica de relatorios em JSON e PDF."""
from __future__ import annotations

import json
from pathlib import Path


class RelatorioInvalido(ValueError):
    """Levantada quando o relatorio nao atende ao esquema minimo."""


_CAMPOS_OBRIGATORIOS = (
    "titulo",
    "periodo",
    "resultados",
    "metricas",
    "alertas",
    "proveniencia",
)


def _validar_relatorio(relatorio: dict) -> None:
    if not isinstance(relatorio, dict):
        raise RelatorioInvalido("o relatorio deve ser um dicionario")
    faltando = [campo for campo in _CAMPOS_OBRIGATORIOS if campo not in relatorio]
    if faltando:
        raise RelatorioInvalido(f"campos obrigatorios ausentes: {faltando}")
    if not isinstance(relatorio["metricas"], dict):
        raise RelatorioInvalido("metricas deve ser um dicionario")
    if not isinstance(relatorio["alertas"], list):
        raise RelatorioInvalido("alertas deve ser uma lista")
    proveniencia = relatorio["proveniencia"]
    if not isinstance(proveniencia, dict):
        raise RelatorioInvalido("proveniencia deve ser um dicionario")
    campos_proveniencia = ("fonte", "versao")
    faltando_proveniencia = [
        campo for campo in campos_proveniencia if not proveniencia.get(campo)
    ]
    if not (proveniencia.get("lote") or proveniencia.get("lote_id")):
        faltando_proveniencia.append("lote")
    if faltando_proveniencia:
        raise RelatorioInvalido(
            f"metadados de proveniencia ausentes: {faltando_proveniencia}"
        )
    try:
        json.dumps(relatorio, ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError) as erro:
        raise RelatorioInvalido(f"relatorio nao e serializavel: {erro}") from erro


def gerar_json(relatorio: dict) -> str:
    """Valida e serializa um relatorio de forma deterministica."""
    _validar_relatorio(relatorio)
    return json.dumps(
        relatorio,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        indent=2,
    )


def _linhas_relatorio(relatorio: dict) -> list[str]:
    secoes = (
        ("Resumo", {"titulo": relatorio["titulo"], "periodo": relatorio["periodo"]}),
        ("Qualidade", relatorio.get("qualidade", {})),
        ("Analise", {"metricas": relatorio["metricas"], "resultados": relatorio["resultados"]}),
        ("Proveniencia", relatorio["proveniencia"]),
        ("Alertas", relatorio["alertas"]),
    )
    linhas = []
    for titulo, conteudo in secoes:
        linhas.append(titulo)
        serializado = json.dumps(conteudo, ensure_ascii=False, sort_keys=True)
        linhas.extend(serializado[i : i + 95] for i in range(0, len(serializado), 95))
        if not serializado:
            linhas.append("{}")
    return linhas


def _escapar_pdf(texto: str) -> bytes:
    return texto.encode("latin-1", "replace").replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")


def _gerar_bytes_pdf(linhas: list[str]) -> bytes:
    por_pagina = 45
    paginas = [linhas[i : i + por_pagina] for i in range(0, len(linhas), por_pagina)] or [[]]
    objetos: list[bytes] = []
    objetos.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objetos.append(b"")
    objetos.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    ids_paginas = []
    for pagina in paginas:
        conteudo = b"BT /F1 10 Tf 50 790 Td "
        comandos = []
        for linha in pagina:
            comandos.append(b"(" + _escapar_pdf(linha) + b") Tj 0 -16 Td")
        conteudo += b" ".join(comandos) + b" ET"
        id_conteudo = len(objetos) + 1
        objetos.append(b"<< /Length " + str(len(conteudo)).encode() + b" >>\nstream\n" + conteudo + b"\nendstream")
        id_pagina = len(objetos) + 1
        objetos.append(
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
            b"/Resources << /Font << /F1 3 0 R >> >> /Contents "
            + str(id_conteudo).encode()
            + b" 0 R >>"
        )
        ids_paginas.append(id_pagina)
    objetos[1] = (
        b"<< /Type /Pages /Kids ["
        + b" ".join(str(identificador).encode() + b" 0 R" for identificador in ids_paginas)
        + b"] /Count "
        + str(len(ids_paginas)).encode()
        + b" >>"
    )
    saida = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for identificador, objeto in enumerate(objetos, start=1):
        offsets.append(len(saida))
        saida.extend(f"{identificador} 0 obj\n".encode())
        saida.extend(objeto)
        saida.extend(b"\nendobj\n")
    inicio_xref = len(saida)
    saida.extend(f"xref\n0 {len(objetos) + 1}\n".encode())
    saida.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        saida.extend(f"{offset:010d} 00000 n \n".encode())
    saida.extend(
        f"trailer\n<< /Size {len(objetos) + 1} /Root 1 0 R >>\nstartxref\n{inicio_xref}\n%%EOF\n".encode()
    )
    return bytes(saida)


def gerar_pdf(relatorio: dict, destino: str | Path) -> Path:
    """Valida e grava um PDF deterministico sem alterar dados de origem."""
    _validar_relatorio(relatorio)
    caminho = Path(destino)
    caminho.write_bytes(_gerar_bytes_pdf(_linhas_relatorio(relatorio)))
    return caminho
