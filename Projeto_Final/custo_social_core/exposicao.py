"""Criticidade ajustada por exposicao (item 4 do escopo).

Um trecho de custo alto pode ser apenas movimentado. Dividir o custo social pela
exposicao de trafego (VMDa) separa o corredor caro do corredor de fato letal. O
VMDa vem do PNCT/VMDa, no mesmo referenciamento do SNV.

Contrato (EARS):
- QUANDO o segmento tem VMDa e extensao, o sistema DEVE calcular o custo por
  veiculo-km do ano.
- SE o segmento nao tem posto de contagem, o sistema DEVE marcar a exposicao como
  imputada, e a imputacao DEVE ser declarada no resultado, nunca silenciosa.
"""
from __future__ import annotations

from . import config


def veiculos_km_ano(vmda: float, extensao_km: float, dias: int = config.DIAS_ANO) -> float:
    """Exposicao anual do segmento em veiculos-km.

    Args:
        vmda: volume medio diario anual (veiculos/dia).
        extensao_km: extensao do segmento (km).
        dias: dias do ano.

    Returns:
        Exposicao em veiculos-km no ano.
    """
    return vmda * extensao_km * dias


def custo_por_exposicao(custo_social: float, vmda: float, extensao_km: float,
                        dias: int = config.DIAS_ANO) -> float:
    """Custo social por veiculo-km do segmento (leitura de risco).

    Raises:
        ValueError: se a exposicao for nula, caso em que a divisao nao tem sentido
            e o segmento deve ser tratado por imputacao declarada, nao por divisao.
    """
    exposicao = veiculos_km_ano(vmda, extensao_km, dias)
    if exposicao <= 0:
        raise ValueError("exposicao nula: use imputacao declarada, nao divisao")
    return custo_social / exposicao


def custo_por_km(custo_social: float, extensao_km: float) -> float:
    """Custo social por quilometro do segmento (leitura de volume)."""
    if extensao_km <= 0:
        raise ValueError("extensao deve ser positiva")
    return custo_social / extensao_km


def ranquear(segmentos: list[dict], chave: str, decrescente: bool = True) -> list[dict]:
    """Ordena os segmentos por uma chave de criticidade.

    Args:
        segmentos: registros de segmento com metricas ja calculadas.
        chave: nome da metrica de ordenacao (ex.: "custo_por_km",
            "custo_por_exposicao").
        decrescente: do mais critico ao menos critico.

    Returns:
        Os segmentos ordenados.
    """
    return sorted(segmentos, key=lambda s: s[chave], reverse=decrescente)
