"""Custo social por ocorrencia: o produto escalar C . M do modelo aditivo do IPEA.

O custo de um sinistro e a soma dos custos medios de cada componente elementar
presente nele, sem ganho de escala:

    custo(i) = C(i) . M(s)

onde C(i) conta pessoas por gravidade e veiculos por classe na ocorrencia i, e
M(s) traz o custo medio padrao, na coluna da gravidade s DA OCORRENCIA.

Os parametros (vetor M, mapeamento, deflator) ficam em vetor_m.py, que e dado de
configuracao. Aqui fica apenas a logica. Spec em
openspec/changes/calculo-custo/, decisoes no ADR-011, memoria de calculo em
docs/memoria-calculo-CM.md.
"""
from __future__ import annotations

from dataclasses import dataclass

from . import vetor_m as vm


class GravidadeDesconhecida(Exception):
    """A classificacao do acidente nao e uma das tres colunas do vetor M."""


class TipoVeiculoNaoMapeado(Exception):
    """O tipo de veiculo da PRF nao consta da tabela de mapeamento."""


@dataclass(frozen=True)
class ResultadoCusto:
    """Custo de uma ocorrencia, decomposto para nao ser recalculado a jusante."""
    total: float
    subtotal_pessoas: float
    subtotal_veiculos: float
    subtotal_institucional: float
    pessoas_sem_gravidade: int
    categoria: str
    base_monetaria: str


def _valida_gravidade(gravidade: str) -> None:
    if gravidade not in vm.GRAVIDADES_OCORRENCIA:
        raise GravidadeDesconhecida(
            f"'{gravidade}' nao e uma das colunas do vetor M: {vm.GRAVIDADES_OCORRENCIA}"
        )


def para_junho_2026(valor_dez2014: float) -> float:
    """Traz um valor de dezembro de 2014 para junho de 2026 pelo IPCA acumulado."""
    return valor_dez2014 * vm.DEFLATOR_DEZ2014_JUN2026


def custo_pessoas(contagem: dict[str, int], gravidade_ocorrencia: str) -> float:
    """Custo dos componentes associados as pessoas, em R$ de dezembro de 2014.

    Args:
        contagem: pessoas por gravidade da vitima (ileso, ferido_leve,
            ferido_grave, obito, nao_informado).
        gravidade_ocorrencia: a coluna do vetor M.

    Raises:
        GravidadeDesconhecida: se a coluna nao existir.
    """
    _valida_gravidade(gravidade_ocorrencia)
    return sum(
        n * vm.M_PESSOAS[g][gravidade_ocorrencia]
        for g, n in contagem.items()
        if g in vm.M_PESSOAS
    )


def contar_caminhoes(contagem_por_tipo: dict[str, int]) -> int:
    """Conta caminhoes pela regra de composicao (ADR-011, decisao 3).

    O semirreboque e o reboque integram a composicao da unidade tratora e nao
    recebem valor proprio. A carreta sem tratora registrada vale um caminhao,
    porque a tratora existiu e nao foi anotada.

        n = tratoras            se tratoras > 0   (absorve o bitrem)
        n = 1                   se tratoras = 0 e ha carreta
        n = 0                   caso contrario
    """
    tratoras = sum(contagem_por_tipo.get(t, 0) for t in vm.UNIDADES_TRATORAS)
    carretas = sum(contagem_por_tipo.get(t, 0) for t in vm.UNIDADES_REBOCADAS)
    if tratoras > 0:
        return tratoras
    return 1 if carretas > 0 else 0


def contar_por_classe(contagem_por_tipo: dict[str, int]) -> dict[str, int]:
    """Agrega os tipos da PRF nas sete classes do IPEA, com a regra de composicao.

    Raises:
        TipoVeiculoNaoMapeado: se algum tipo nao constar do mapeamento. Falhar e
            deliberado: a classe Outros custa mais que o caminhao no acidente com
            vitimas, e absorver o desconhecido nela inflaria o custo em silencio.
    """
    por_classe: dict[str, int] = {}
    for tipo, n in contagem_por_tipo.items():
        if tipo in vm.UNIDADES_TRATORAS or tipo in vm.UNIDADES_REBOCADAS:
            continue  # tratado pela regra de composicao
        classe = vm.MAPA_VEICULOS.get(tipo)
        if classe is None:
            raise TipoVeiculoNaoMapeado(
                f"tipo '{tipo}' fora do mapeamento; atualize vetor_m.MAPA_VEICULOS"
            )
        por_classe[classe] = por_classe.get(classe, 0) + n

    caminhoes = contar_caminhoes(contagem_por_tipo)
    if caminhoes:
        por_classe["Caminhões"] = por_classe.get("Caminhões", 0) + caminhoes
    return por_classe


def custo_veiculos(contagem_por_tipo: dict[str, int], gravidade_ocorrencia: str) -> float:
    """Custo dos componentes associados aos veiculos, em R$ de dezembro de 2014."""
    _valida_gravidade(gravidade_ocorrencia)
    return sum(
        n * vm.M_VEICULOS[classe][gravidade_ocorrencia]
        for classe, n in contar_por_classe(contagem_por_tipo).items()
    )


def custo_institucional(gravidade_ocorrencia: str) -> float:
    """Bloco institucional e patrimonial, uma vez por ocorrencia."""
    _valida_gravidade(gravidade_ocorrencia)
    return vm.M_INSTITUCIONAL[gravidade_ocorrencia]


def categoria_da_ocorrencia(contagem_pessoas: dict[str, int]) -> str:
    """Classifica a ocorrencia pela vitima mais grave presente."""
    if contagem_pessoas.get("obito", 0) > 0:
        return "com_obito"
    if contagem_pessoas.get("ferido_grave", 0) > 0:
        return "com_vitima_grave"
    if contagem_pessoas.get("ferido_leve", 0) > 0:
        return "com_vitima_leve"
    return "sem_vitimas"


def custo_ocorrencia(
    vetor_c: dict[str, int], gravidade_ocorrencia: str, aplicar_deflator: bool = True
) -> ResultadoCusto:
    """Custo total de uma ocorrencia, pelo produto escalar C . M.

    O vetor C mistura, no mesmo dicionario, as gravidades das pessoas e os tipos
    de veiculo, como sai da ingestao. A separacao acontece aqui.

    Args:
        vetor_c: contagens por gravidade da vitima e por tipo de veiculo.
        gravidade_ocorrencia: a coluna do vetor M.
        aplicar_deflator: quando falso, devolve em R$ de dezembro de 2014.

    Returns:
        O custo decomposto, com os tres subtotais e a lacuna declarada.
    """
    _valida_gravidade(gravidade_ocorrencia)

    pessoas = {g: n for g, n in vetor_c.items() if g in vm.M_PESSOAS}
    veiculos = {t: n for t, n in vetor_c.items() if t not in vm.M_PESSOAS}

    sp = custo_pessoas(pessoas, gravidade_ocorrencia)
    sv = custo_veiculos(veiculos, gravidade_ocorrencia)
    si = custo_institucional(gravidade_ocorrencia)
    total = sp + sv + si

    if aplicar_deflator:
        # O deflator multiplica o TOTAL, uma vez so (design.md).
        sp, sv, si, total = (para_junho_2026(x) for x in (sp, sv, si, total))

    return ResultadoCusto(
        total=total,
        subtotal_pessoas=sp,
        subtotal_veiculos=sv,
        subtotal_institucional=si,
        pessoas_sem_gravidade=int(pessoas.get("nao_informado", 0)),
        categoria=categoria_da_ocorrencia(pessoas),
        base_monetaria=vm.BASE_MONETARIA if aplicar_deflator else "dez/2014",
    )
