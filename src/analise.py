"""Análise estatística de apoio (Etapa 2 do harness — desenvolvida via TDD).

Reúne funções pequenas e verificáveis usadas pelo validador de qualidade e,
adiante, pelo piloto de custo social (detecção de outliers, nível de risco).
"""
from __future__ import annotations

import statistics


def detectar_outliers_iqr(valores: list[float], k: float = 1.5) -> list[int]:
    """Detecta outliers pela regra do IQR e devolve os índices na lista original.

    Um valor é outlier se estiver abaixo de Q1 - k*IQR ou acima de Q3 + k*IQR.
    Com menos de quatro pontos o IQR não é informativo, e a função devolve [].

    Args:
        valores: lista de números.
        k: multiplicador do IQR (1,5 é o padrão de Tukey).

    Returns:
        Índices (na ordem original) dos valores considerados outliers.
    """
    if len(valores) < 4:
        return []
    q1, _mediana, q3 = statistics.quantiles(valores, n=4, method="inclusive")
    iqr = q3 - q1
    if iqr == 0:
        return []
    limite_inf = q1 - k * iqr
    limite_sup = q3 + k * iqr
    return [i for i, v in enumerate(valores) if v < limite_inf or v > limite_sup]


def nivel_risco(taxa: float) -> str:
    """Classifica o nivel de risco de um trecho pela taxa de sinistros.

    NOTA (Etapa 2, tarefa SEM TDD): escrita direto, sem teste antes. Nao valida
    entrada invalida (taxa negativa) — lacuna revelada por teste posterior.
    """
    if taxa > 1.0:
        return "alto"
    elif taxa > 0.5:
        return "medio"
    else:
        return "baixo"
