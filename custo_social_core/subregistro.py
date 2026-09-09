"""Correcao de subregistro no mapa (item 5 do escopo).

A PRF registra menos obitos que o SIM em parte da malha. Cada segmento aparece em
dois valores: o observado pela PRF e o corrigido pelo fator do cenario, para o mapa
nao ler ausencia de registro como ausencia de custo.

Contrato (EARS):
- QUANDO um valor observado e um cenario sao dados, o sistema DEVE devolver o valor
  corrigido pelo fator do cenario.
- O cenario DEVE ser um dos declarados em config.FATOR_SUBREGISTRO (piso, central,
  teto).
"""
from __future__ import annotations

from . import config


def fator(cenario: str = config.CENARIO_SUBREGISTRO_PADRAO) -> float:
    """Fator de correcao do cenario.

    Raises:
        KeyError: se o cenario nao estiver declarado em config.
    """
    if cenario not in config.FATOR_SUBREGISTRO:
        raise KeyError(
            f"cenario '{cenario}' nao declarado; use {list(config.FATOR_SUBREGISTRO)}"
        )
    return config.FATOR_SUBREGISTRO[cenario]


def corrigir(valor_observado: float, cenario: str = config.CENARIO_SUBREGISTRO_PADRAO) -> float:
    """Aplica o fator de subregistro ao valor observado da PRF.

    Args:
        valor_observado: contagem ou custo observado pela PRF.
        cenario: piso, central ou teto.

    Returns:
        O valor corrigido.
    """
    return valor_observado * fator(cenario)
