"""Custo hibrido em quatro categorias (item 1 do escopo).

O Ipea da o custo por ocorrencia em tres classes (ancora). O refino decompoe a
classe de feridos em leve e grave usando a razao de custo observada na LAI (SIH
para internacao do grave, INSS para perda de producao), chegando a quatro
categorias por vitima. A decomposicao triangula contra o total do Ipea; ela NAO
soma sobre o valor do Ipea, para evitar dupla contagem.

Contrato (EARS):
- QUANDO uma ocorrencia e sem vitimas, o custo DEVE ser o valor de dano material.
- QUANDO uma ocorrencia tem feridos, o custo DEVE somar o custo de cada vitima por
  gravidade (leve, grave), e a soma das vitimas DEVE reproduzir a classe do Ipea
  dentro da tolerancia de triangulacao.
- QUANDO uma ocorrencia tem obito, o custo DEVE somar o valor por vitima fatal.
"""
from __future__ import annotations

from dataclasses import dataclass

from . import config


@dataclass(frozen=True)
class CustoVitima:
    """Custo unitario por gravidade, em R$ correntes, ancorado em desembolso."""
    sem_feridos: float   # dano material por ocorrencia (PRF/DNIT)
    ferido_leve: float
    ferido_grave: float
    obito: float


def custo_ocorrencia(
    n_leves: int, n_graves: int, n_mortos: int, houve_dano: bool, tabela: CustoVitima
) -> float:
    """Custo social de uma ocorrencia pela contagem de vitimas por gravidade.

    A contagem vem das colunas por pessoa da PRF (feridos_leves, feridos_graves,
    mortos). O dano material entra uma vez por ocorrencia quando nao ha vitima.

    Args:
        n_leves: numero de feridos leves na ocorrencia.
        n_graves: numero de feridos graves na ocorrencia.
        n_mortos: numero de mortos na ocorrencia.
        houve_dano: se ha dano material a contar (ocorrencia sem vitima).
        tabela: custos unitarios por gravidade.

    Returns:
        Custo social da ocorrencia em R$.
    """
    total = 0.0
    total += n_leves * tabela.ferido_leve
    total += n_graves * tabela.ferido_grave
    total += n_mortos * tabela.obito
    if n_leves == 0 and n_graves == 0 and n_mortos == 0 and houve_dano:
        total += tabela.sem_feridos
    return total


def razao_leve_grave(custo_leve: float, custo_grave: float) -> float:
    """Razao de custo entre ferido grave e ferido leve, para auditar a decomposicao.

    Serve de verificacao: a razao observada (SIH + INSS) deve ficar coerente com a
    proporcao leve/grave da PRF ao reproduzir o total da classe de feridos do Ipea.
    """
    if custo_leve <= 0:
        raise ValueError("custo do ferido leve deve ser positivo")
    return custo_grave / custo_leve


def validar_triangulacao(
    custo_refinado_classe_feridos: float,
    custo_ipea_com_feridos: float = config.CUSTO_IPEA_OCORRENCIA["com_feridos"],
    tolerancia: float = 0.15,
) -> bool:
    """Confere se o custo refinado da classe de feridos triangula com o Ipea.

    A decomposicao e aceita quando o custo medio refinado por ocorrencia com feridos
    fica dentro da tolerancia relativa ao valor do Ipea. Fora disso, a razao de custo
    ou a proporcao leve/grave precisa de revisao.
    """
    if custo_ipea_com_feridos <= 0:
        raise ValueError("valor do Ipea deve ser positivo")
    desvio = abs(custo_refinado_classe_feridos - custo_ipea_com_feridos) / custo_ipea_com_feridos
    return desvio <= tolerancia
