"""Referenciamento linear no Sistema Nacional de Viacao (SNV).

Ancora cada sinistro ao segmento da malha cuja faixa de quilometragem o contem,
na safra vigente no ano do sinistro. O segmento carrega o regime de administracao,
que separa a malha do DNIT da concedida a ANTT.

Spec em openspec/changes/consolidacao-e-snv/specs/snv-referenciamento/.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

# A planilha do DNIT traz duas linhas de metadados antes do cabecalho.
LINHA_CABECALHO = 2

# Colunas obrigatorias, no rotulo original do DNIT -> nome normalizado.
COLUNAS = {
    "BR": "br", "UF": "uf", "Tipo de trecho": "tipo_trecho", "Código": "codigo",
    "km inicial": "km_inicial", "km final": "km_final", "Extensão": "extensao",
    "Administração": "administracao", "Jurisdição": "jurisdicao",
}

# Regime de administracao (ADR-011 e proposal da mudanca).
REGIMES = {"Federal": "DNIT", "Concessão Federal": "ANTT"}

# Preferencia no desempate de coincidentes: menor e melhor.
# A jurisdicao vem primeiro porque a base da PRF cobre a malha federal; ancorar
# num estadual coincidente atribuiria custo federal a via estadual.
ORDEM_JURISDICAO = {"Federal": 0}
ORDEM_TIPO = {"Eixo Principal": 0, "Contorno": 1, "Anel": 2, "Acesso": 3}


class CabecalhoInesperado(Exception):
    """A terceira linha da planilha nao traz os rotulos de coluna esperados."""


class SafraIndisponivel(Exception):
    """Nao ha safra do SNV vigente no ano do sinistro."""


@dataclass(frozen=True)
class Ancoragem:
    """Resultado da ancoragem de uma ocorrencia."""
    ancorada: bool
    codigo: str | None
    houve_desempate: bool
    motivo: str


def _num(serie: pd.Series) -> pd.Series:
    """Converte quilometragem para numero, aceitando virgula ou ponto decimal.

    As safras nao sao homogeneas: a de novembro de 2025 grava '2,4' e as
    anteriores gravam '2.4'. Sem esta normalizacao a safra inteira vira nulo e
    nenhuma ocorrencia daquele ano ancora.
    """
    return pd.to_numeric(
        serie.astype("string").str.strip().str.replace(",", ".", regex=False),
        errors="coerce",
    )


def ler_safra(caminho: str | Path, uf: str | None = None) -> pd.DataFrame:
    """Le a planilha de uma safra do SNV e normaliza as colunas obrigatorias.

    O cabecalho fica na terceira linha, posicao fixa. Procurar o cabecalho
    aceitaria em silencio uma planilha de formato diferente.

    Raises:
        CabecalhoInesperado: se faltar qualquer coluna obrigatoria.
    """
    d = pd.read_excel(caminho, header=LINHA_CABECALHO)
    d.columns = [str(c).strip() for c in d.columns]

    faltando = [c for c in COLUNAS if c not in d.columns]
    if faltando:
        raise CabecalhoInesperado(
            f"colunas ausentes na linha {LINHA_CABECALHO + 1}: {faltando}"
        )

    d = d[list(COLUNAS)].rename(columns=COLUNAS)
    d["uf"] = d["uf"].astype(str).str.strip()
    d["codigo"] = d["codigo"].astype(str).str.strip()
    d["br"] = pd.to_numeric(d["br"], errors="coerce").astype("Int64")
    for c in ("km_inicial", "km_final", "extensao"):
        d[c] = _num(d[c])
    d["regime"] = d["administracao"].map(regime)

    if uf is not None:
        d = d[d["uf"] == uf]
    return d.reset_index(drop=True)


def selecionar_safra(ano_sinistro: int, safras: list[str]) -> str:
    """Escolhe a safra vigente no ano do sinistro.

    Vigente e a mais recente cujo ano de referencia nao ultrapassa o ano do
    sinistro. Usar safra posterior deslocaria o ponto, porque a quilometragem
    muda entre safras.

    Raises:
        SafraIndisponivel: se nao houver safra igual ou anterior.
    """
    candidatas = [s for s in safras if int(str(s)[:4]) <= ano_sinistro]
    if not candidatas:
        raise SafraIndisponivel(
            f"nenhuma safra do SNV vigente em {ano_sinistro}; disponiveis: {safras}"
        )
    return max(candidatas, key=lambda s: str(s)[:6])


def regime(administracao) -> str:
    """Deriva o regime a partir da administracao do segmento.

    Federal e DNIT, Concessao Federal e ANTT. As demais recebem 'outro' e ficam
    fora da comparacao entre regimes.
    """
    return REGIMES.get(str(administracao).strip(), "outro")


def ancorar(br: int, uf: str, km: float, segmentos: pd.DataFrame) -> Ancoragem:
    """Ancora um ponto (BR, UF, km) ao segmento que o contem.

    Quando mais de um segmento contem o km, caso dos trechos coincidentes, a
    escolha segue a preferencia: jurisdicao federal, eixo principal, menor
    extensao, menor codigo. O desempate fica declarado no resultado.
    """
    cand = segmentos[
        (segmentos["br"] == br)
        & (segmentos["uf"] == uf)
        & (segmentos["km_inicial"] <= km)
        & (segmentos["km_final"] >= km)
    ]
    if cand.empty:
        return Ancoragem(False, None, False, f"km {km} fora da faixa da BR-{br}/{uf}")

    if len(cand) == 1:
        return Ancoragem(True, str(cand.iloc[0]["codigo"]), False, "")

    vazia = pd.Series(index=cand.index, dtype=object)
    ordenado = cand.assign(
        _jur=cand.get("jurisdicao", vazia).map(
            lambda j: ORDEM_JURISDICAO.get(str(j).strip(), 9)),
        _tipo=cand.get("tipo_trecho", vazia).map(
            lambda t: ORDEM_TIPO.get(str(t).strip(), 9)),
    ).sort_values(["_jur", "_tipo", "extensao", "codigo"])
    escolhido = ordenado.iloc[0]
    return Ancoragem(
        True, str(escolhido["codigo"]), True,
        f"{len(cand)} segmentos coincidentes no km {km}; "
        "escolhido por jurisdicao, tipo, extensao e codigo",
    )


def agregar_por_segmento(
    ancoragens: pd.DataFrame, custos: pd.DataFrame, segmentos: pd.DataFrame
) -> pd.DataFrame:
    """Soma o custo das ocorrencias ancoradas em cada segmento.

    O segmento aparece uma unica vez, ainda que ancorado em varias safras: o custo
    soma todas, e a extensao e a da safra mais recente em que ele foi ancorado.
    Repetir por safra somaria a mesma extensao fisica varias vezes e inflaria a
    malha do estado.

    Args:
        ancoragens: colunas `id`, `codigo` e, quando houver, `safra`.
        custos: colunas `id` e `total`.
        segmentos: os segmentos, com `codigo`, `extensao` e, quando houver, `safra`.

    Returns:
        Um registro por segmento, com custo social, extensao e custo por km.
    """
    d = ancoragens.merge(custos, on="id", how="inner")
    g = (d.groupby("codigo", as_index=False)
           .agg(custo_social=("total", "sum"), ocorrencias=("id", "size")))

    atributos = ["br", "uf", "km_inicial", "km_final", "regime", "jurisdicao",
                 "administracao", "tipo_trecho"]
    cols = ["codigo", "extensao"] + [c for c in atributos if c in segmentos.columns]

    if "safra" in segmentos.columns:
        # a safra mais recente em que o segmento foi ancorado define a extensao
        if "safra" in ancoragens.columns:
            recente = (ancoragens.dropna(subset=["codigo"])
                       .groupby("codigo", as_index=False)["safra"].max())
            base = (segmentos[cols + ["safra"]]
                    .merge(recente, on=["codigo", "safra"], how="inner")
                    .drop(columns="safra"))
        else:
            base = (segmentos.sort_values("safra")
                    .drop_duplicates("codigo", keep="last")[cols])
    else:
        base = segmentos[cols].drop_duplicates("codigo")

    g = g.merge(base.drop_duplicates("codigo"), on="codigo", how="left")
    g["custo_por_km"] = g["custo_social"] / g["extensao"]
    return g
