"""Exposicao de trafego (PNCT/VMDa) e criticidade ajustada por exposicao.

Um trecho de custo alto pode ser apenas movimentado. Dividir o custo social pela
exposicao de trafego separa o corredor caro do corredor de fato perigoso.

O arquivo do Plano Nacional de Contagem de Trafego carrega a coluna `vl_codigo`,
que e o mesmo codigo de segmento do SNV: a juncao e por igualdade de codigo, sem
casamento espacial.

Spec em openspec/changes/exposicao-e-saude/specs/exposicao/.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

DIAS_ANO = 365

# Rotulos originais do PNCT -> nomes normalizados.
COLUNAS = {
    "vl_codigo": "codigo", "vl_br": "br", "sg_uf": "uf",
    "vl_km_inic": "km_inicial", "vl_km_fina": "km_final", "vl_extensa": "extensao",
    "VMDa_C": "vmda_c", "VMDa_D": "vmda_d",
}


class AbaDeDadosAusente(Exception):
    """O arquivo do PNCT nao tem aba de dados, ou tem mais de uma."""


def ler_vmda(caminho: str | Path) -> pd.DataFrame:
    """Le o arquivo anual do VMDa, identificando a aba de dados por conteudo.

    O nome da aba muda a cada ano (`SNV_201903A`, `VMDa 2021`,
    `VMDa2025_SNV202401A`), entao a identificacao e por exclusao: a aba de dados
    e a que nao se chama Metadados.

    Raises:
        AbaDeDadosAusente: se nao houver exatamente uma aba de dados.
    """
    x = pd.ExcelFile(caminho)
    candidatas = [s for s in x.sheet_names if s.strip().lower() != "metadados"]
    if len(candidatas) != 1:
        raise AbaDeDadosAusente(
            f"esperava uma aba de dados, encontrei {candidatas or 'nenhuma'}"
        )

    d = pd.read_excel(caminho, sheet_name=candidatas[0])
    d.columns = [str(c).strip() for c in d.columns]
    faltando = [c for c in COLUNAS if c not in d.columns]
    if faltando:
        raise AbaDeDadosAusente(f"aba '{candidatas[0]}' sem as colunas {faltando}")

    d = d[list(COLUNAS)].rename(columns=COLUNAS)
    d["codigo"] = d["codigo"].astype(str).str.strip()
    d["uf"] = d["uf"].astype(str).str.strip()
    d["br"] = pd.to_numeric(d["br"], errors="coerce").astype("Int64")
    for c in ("km_inicial", "km_final", "extensao", "vmda_c", "vmda_d"):
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d["safra_vmda"] = candidatas[0]
    return d.reset_index(drop=True)


def volume_total(vmda_c, vmda_d) -> tuple[float | None, bool]:
    """Soma os dois sentidos e declara se a medicao veio completa.

    Quando um sentido falta, o presente e usado e a incompletude e declarada:
    descartar o segmento perderia trafego que existe. Quando os dois faltam, o
    resultado e nulo declarado, e NAO uma imputacao silenciosa.

    Returns:
        O volume total e um sinalizador de medicao completa.
    """
    c = None if pd.isna(vmda_c) else float(vmda_c)
    d = None if pd.isna(vmda_d) else float(vmda_d)
    if c is None and d is None:
        return None, False
    if c is None or d is None:
        return (c if c is not None else d), False
    return c + d, True


def agregar_por_segmento(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega os postos de contagem de cada segmento pela media.

    O mesmo codigo aparece varias vezes porque ha mais de um posto no trecho, com
    volumes distintos. A media representa o trafego tipico ao longo do segmento,
    que e o que a exposicao em veiculos-km pede. O maximo descreveria o ponto mais
    movimentado, e a soma contaria o mesmo fluxo mais de uma vez.
    """
    d = df.copy()
    tot = d.apply(lambda r: volume_total(r["vmda_c"], r["vmda_d"]), axis=1)
    d["volume"] = [v for v, _ in tot]
    d["completo"] = [c for _, c in tot]

    g = (d.groupby("codigo", as_index=False)
           .agg(vmda=("volume", "mean"),
                n_postos=("volume", "count"),
                sentidos_completos=("completo", "all"),
                br=("br", "first"), uf=("uf", "first"),
                extensao=("extensao", "first"),
                safra_vmda=("safra_vmda", "first")))
    return g


def veiculos_km_ano(vmda: float, extensao: float, dias: int = DIAS_ANO) -> float:
    """Exposicao anual do segmento, em veiculos-quilometro."""
    return vmda * extensao * dias


def criticidade(custo_social: float, vmda, extensao: float,
                dias: int = DIAS_ANO) -> float | None:
    """Custo social por veiculo-quilometro.

    Returns:
        O custo por veiculo-km, ou None quando nao ha exposicao medida. O nulo e
        declarado: o segmento continua no ranque por custo por quilometro, apenas
        sem a leitura por exposicao.
    """
    if vmda is None or pd.isna(vmda) or vmda <= 0 or extensao <= 0:
        return None
    return custo_social / veiculos_km_ano(float(vmda), extensao, dias)


def custo_por_km(custo_social: float, extensao: float) -> float:
    """Custo social por quilometro do segmento (leitura de volume)."""
    if extensao <= 0:
        raise ValueError("extensao deve ser positiva")
    return custo_social / extensao
