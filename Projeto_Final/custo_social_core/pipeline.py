"""Orquestrador do nucleo: de uma UF a uma tabela de custo e criticidade por segmento.

Este e o unico modulo que compoe os demais. Rodar o piloto RN e chamar
rodar(uf='RN'); rodar o Brasil e chamar a mesma funcao com outra UF. A leitura dos
dados (PRF, SNV, VMDa, LAI) e injetada por um provedor, para manter o nucleo
testavel sem os arquivos grandes e para o repositorio privado reusar o mesmo codigo
com os dados nacionais.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from . import config, custo, exposicao, referenciamento, subregistro


class ProvedorDeDados(Protocol):
    """Contrato de leitura de dados, implementado na fase 2 (RN) e no repo BR."""

    def safras_snv(self) -> list[str]: ...
    def segmentos_snv(self, safra: str, uf: str) -> list[referenciamento.SegmentoSNV]: ...
    def sinistros(self, uf: str) -> list[dict]: ...   # br, km, ano, n_leves, n_graves, n_mortos, houve_dano
    def vmda_segmento(self, safra: str, br: int, km_inicial: float) -> float | None: ...
    def tabela_custo_vitima(self, uf: str) -> custo.CustoVitima: ...


@dataclass
class ResultadoSegmento:
    """Uma linha do mapa: custo e criticidade de um segmento."""
    br: int
    km_inicial: float
    km_final: float
    extensao_km: float
    custo_social: float = 0.0
    custo_corrigido: float = 0.0
    custo_por_km: float = 0.0
    custo_por_exposicao: float | None = None
    exposicao_imputada: bool = False
    corredor_destaque: bool = False


@dataclass
class ResultadoPiloto:
    uf: str
    cenario_subregistro: str
    segmentos: list[ResultadoSegmento] = field(default_factory=list)


def rodar(
    provedor: ProvedorDeDados,
    uf: str = config.UF,
    cenario_subregistro: str = config.CENARIO_SUBREGISTRO_PADRAO,
) -> ResultadoPiloto:
    """Executa o pipeline para uma UF e devolve a tabela por segmento.

    Passos: casa a safra do SNV com o ano de cada sinistro, ancora o sinistro ao
    segmento, soma o custo por gravidade, aplica a correcao de subregistro e calcula
    as duas leituras de criticidade (por km e por exposicao).

    Args:
        provedor: fonte de dados que implementa ProvedorDeDados.
        uf: unidade da federacao a processar (o unico parametro de escala).
        cenario_subregistro: piso, central ou teto.

    Returns:
        O resultado por segmento, pronto para o mapa e a tabela.
    """
    corredores = set(config.CORREDORES_POR_UF.get(uf, []))
    safras = provedor.safras_snv()
    tabela_custo = provedor.tabela_custo_vitima(uf)

    # Acumula custo por segmento, identificado pela chave (safra, br, km_inicial).
    acumulado: dict[tuple[str, int, float], ResultadoSegmento] = {}

    for sin in provedor.sinistros(uf):
        safra = referenciamento.selecionar_safra(sin["ano"], safras)
        segmentos = provedor.segmentos_snv(safra, uf)
        try:
            seg = referenciamento.ancorar(sin["br"], uf, sin["km"], segmentos)
        except referenciamento.ForaDaFaixa:
            continue  # sinistro sem segmento na safra: registrado a parte na fase 2

        chave = (safra, seg.br, seg.km_inicial)
        linha = acumulado.get(chave)
        if linha is None:
            linha = ResultadoSegmento(
                br=seg.br, km_inicial=seg.km_inicial, km_final=seg.km_final,
                extensao_km=seg.extensao_km, corredor_destaque=seg.br in corredores,
            )
            acumulado[chave] = linha

        linha.custo_social += custo.custo_ocorrencia(
            sin["n_leves"], sin["n_graves"], sin["n_mortos"], sin["houve_dano"], tabela_custo
        )

    # Fecha as metricas por segmento.
    resultado = ResultadoPiloto(uf=uf, cenario_subregistro=cenario_subregistro)
    for (safra, br, km_ini), linha in acumulado.items():
        linha.custo_corrigido = subregistro.corrigir(linha.custo_social, cenario_subregistro)
        linha.custo_por_km = exposicao.custo_por_km(linha.custo_social, linha.extensao_km)
        vmda = provedor.vmda_segmento(safra, br, km_ini)
        if vmda and vmda > 0:
            linha.custo_por_exposicao = exposicao.custo_por_exposicao(
                linha.custo_social, vmda, linha.extensao_km
            )
        else:
            linha.exposicao_imputada = True  # declarada, tratada na fase 3
        resultado.segmentos.append(linha)

    return resultado
