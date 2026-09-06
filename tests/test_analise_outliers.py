import pytest

from src.analise import detectar_outliers_iqr


def test_sem_outlier_retorna_vazio():
    assert detectar_outliers_iqr([10, 11, 12, 13, 14, 15]) == []


def test_detecta_outlier_alto():
    # 100 e o outlier no fim
    idx = detectar_outliers_iqr([10, 11, 12, 13, 14, 100])
    assert idx == [5]


def test_detecta_outlier_baixo():
    idx = detectar_outliers_iqr([-100, 10, 11, 12, 13, 14])
    assert idx == [0]


def test_lista_vazia_ou_curta_retorna_vazio():
    assert detectar_outliers_iqr([]) == []
    assert detectar_outliers_iqr([5, 5, 5]) == []


def test_todos_iguais_sem_outlier():
    assert detectar_outliers_iqr([7, 7, 7, 7, 7, 7]) == []
