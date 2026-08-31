"""Funcionalidade 3 — Parser de tabela de uma resposta da LAI em PDF.

A logica de normalizacao (transformar linhas brutas extraidas em registros) fica
separada da leitura do PDF, para poder ser testada sem um arquivo PDF real. A
funcao extrair_tabela_pdf usa pdfplumber e delega a normalizacao a normalizar_linhas.
"""
from __future__ import annotations

from pathlib import Path


class TabelaVazia(Exception):
    """Levantada quando nenhuma linha util e encontrada no PDF."""


def normalizar_linhas(linhas: list[list[str]]) -> list[dict]:
    """Converte linhas brutas (a primeira e o cabecalho) em registros.

    Regras: usa a primeira linha como cabecalho; ignora linhas totalmente vazias;
    completa com "" as celulas faltantes e descarta as excedentes.

    Args:
        linhas: lista de linhas, cada uma lista de celulas (texto).

    Returns:
        Lista de dicionarios (um por linha de dados).

    Raises:
        TabelaVazia: se nao houver cabecalho ou nenhuma linha de dados.
    """
    linhas = [ln for ln in linhas if any((c or "").strip() for c in ln)]
    if len(linhas) < 2:
        raise TabelaVazia("PDF sem cabecalho ou sem linhas de dados")

    cabecalho = [(c or "").strip() for c in linhas[0]]
    registros = []
    for ln in linhas[1:]:
        valores = [(c or "").strip() for c in ln]
        valores = (valores + [""] * len(cabecalho))[: len(cabecalho)]
        registros.append(dict(zip(cabecalho, valores)))
    return registros


def extrair_tabela_pdf(caminho_pdf: str | Path, pagina: int = 0) -> list[dict]:
    """Extrai a primeira tabela de uma pagina do PDF e normaliza em registros.

    Args:
        caminho_pdf: caminho do PDF da resposta da LAI.
        pagina: indice da pagina (0-based).

    Returns:
        Lista de registros normalizados.
    """
    import pdfplumber  # importado aqui para nao exigir a dependencia nos testes da logica pura

    with pdfplumber.open(str(caminho_pdf)) as pdf:
        tabela = pdf.pages[pagina].extract_table()
    if not tabela:
        raise TabelaVazia("nenhuma tabela encontrada na pagina")
    return normalizar_linhas(tabela)
