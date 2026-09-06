"""Referenciamento linear: ancora cada sinistro ao segmento do SNV (item 2).

Contrato (EARS):
- QUANDO um sinistro tem BR, UF e km, o sistema DEVE ancora-lo ao segmento do SNV
  cuja faixa [km_inicial, km_final] contem o km, na mesma BR e UF.
- QUANDO o ano do sinistro e informado, o sistema DEVE usar a safra do SNV vigente
  naquele ano, e NAO uma safra posterior.
- SE nenhum segmento contiver o km, o sistema DEVE devolver None, sem aproximar.

A logica pura (selecao de safra e ancoragem) fica aqui, testavel sem os arquivos
grandes do SNV. A leitura das planilhas do SNV entra na fase 2, por uma funcao de
carga que devolve a lista de segmentos no formato abaixo.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SegmentoSNV:
    """Um segmento da malha, na safra a que pertence."""
    safra: str          # ex.: "202001A"
    br: int
    uf: str
    km_inicial: float
    km_final: float
    extensao_km: float
    superficie: str = ""


class ForaDaFaixa(Exception):
    """Levantada quando nenhum segmento contem o km do sinistro."""


def selecionar_safra(ano_sinistro: int, safras: list[str]) -> str:
    """Escolhe a safra do SNV vigente no ano do sinistro.

    A safra vigente e a mais recente cujo ano de referencia nao ultrapassa o ano
    do sinistro. Casar a safra com o ano evita ancorar em km que mudou de tracado.

    Args:
        ano_sinistro: ano do sinistro (ex.: 2019).
        safras: rotulos de safra disponiveis (ex.: ["201811A", "202001A", ...]).

    Returns:
        O rotulo da safra vigente.

    Raises:
        ValueError: se nao houver safra igual ou anterior ao ano do sinistro.
    """
    candidatas = [s for s in safras if int(s[:4]) <= ano_sinistro]
    if not candidatas:
        raise ValueError(
            f"nenhuma safra do SNV vigente em {ano_sinistro}; safras: {safras}"
        )
    return max(candidatas, key=lambda s: s[:6])


def ancorar(br: int, uf: str, km: float, segmentos: list[SegmentoSNV]) -> SegmentoSNV:
    """Ancora um ponto (BR, UF, km) ao segmento que o contem.

    Args:
        br: numero da BR.
        uf: sigla da unidade da federacao.
        km: quilometro do sinistro.
        segmentos: segmentos de uma unica safra.

    Returns:
        O segmento cuja faixa contem o km.

    Raises:
        ForaDaFaixa: se nenhum segmento da BR/UF contiver o km.
    """
    for seg in segmentos:
        if seg.br == br and seg.uf == uf and seg.km_inicial <= km <= seg.km_final:
            return seg
    raise ForaDaFaixa(f"BR-{br}/{uf} km {km} fora de qualquer segmento da safra")
