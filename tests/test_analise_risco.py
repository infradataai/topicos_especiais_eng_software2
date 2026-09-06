import pytest

from src.analise import nivel_risco


def test_niveis_normais():
    assert nivel_risco(2.0) == "alto"
    assert nivel_risco(0.7) == "medio"
    assert nivel_risco(0.1) == "baixo"


@pytest.mark.xfail(reason="lacuna da tarefa sem TDD: taxa negativa e invalida e deveria ser recusada, mas passa como 'baixo'")
def test_taxa_negativa_deveria_recusar():
    # Um fluxo TDD teria fixado este caso de borda ANTES de implementar.
    with pytest.raises(ValueError):
        nivel_risco(-0.5)
