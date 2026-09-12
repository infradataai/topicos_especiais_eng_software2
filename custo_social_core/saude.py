"""Agregados do DATASUS: obitos do SIM e internacoes do SIH.

Servem a dois propositos. Os obitos por acidente de transporte medem quanto da
mortalidade de transito ocorre fora da malha federal, e as internacoes por causa
externa dao o lastro da completude do registro de ferido grave.

Ha uma distincao de metodo que este modulo protege. A razao entre os obitos da
PRF e os do SIM mede COBERTURA DE JURISDICAO, porque a PRF cobre a malha federal
e o SIM cobre todas as vias. Ela NAO e fator de sub-registro. Confundir as duas
coisas foi o defeito encontrado na auditoria da planilha V07, e por isso a funcao
que devolve a cobertura recusa ser usada como fator de correcao.

Spec em openspec/changes/exposicao-e-saude/specs/saude/.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROTULO_COBERTURA = "cobertura de jurisdicao"


class UsoIndevidoDeCobertura(Exception):
    """A cobertura de jurisdicao foi pedida como fator de sub-registro."""


def ler_agregado(caminho: str | Path) -> pd.DataFrame:
    """Le um CSV agregado do DATASUS.

    Os arquivos vem com marca de ordem de byte no inicio do cabecalho. Sem o
    tratamento, a primeira coluna passa a se chamar '\\ufeffuf' e nenhuma consulta
    por nome funciona. A codificacao utf-8-sig consome a marca.
    """
    d = pd.read_csv(caminho, encoding="utf-8-sig")
    d.columns = [str(c).strip().lstrip("﻿") for c in d.columns]
    return d


def obitos(df: pd.DataFrame, uf: str, ano: int) -> dict:
    """Obitos por acidente de transporte de uma UF num ano.

    Returns:
        Total, parcela em estabelecimento de saude e parcela em via publica.
    """
    linha = df[(df["uf"] == uf) & (df["ano"] == ano)]
    if linha.empty:
        raise KeyError(f"sem registro de obitos para {uf} em {ano}")
    r = linha.iloc[0]
    return {c: int(r[c]) for c in df.columns if c not in ("uf", "ano")}


def internacoes_do_ano(df: pd.DataFrame, uf: str, ano: int) -> int:
    """Soma as internacoes por causa externa de uma UF ao longo do ano."""
    return int(df[(df["uf"] == uf) & (df["ano"] == ano)]["internacoes"].sum())


def cobertura_jurisdicao(prf: pd.DataFrame, sim: pd.DataFrame) -> pd.DataFrame:
    """Razao entre os obitos da PRF e os do SIM, por UF e ano.

    A razao mede quanto da mortalidade de transito ocorre em rodovia federal. Ela
    vem rotulada, para nao circular como fator de sub-registro.

    Args:
        prf: colunas `uf`, `ano`, `obitos_prf`.
        sim: colunas `uf`, `ano`, `obitos_transporte`.
    """
    d = prf.merge(sim, on=["uf", "ano"], how="inner")
    d["cobertura_jurisdicao"] = d["obitos_prf"] / d["obitos_transporte"]
    d["rotulo"] = ROTULO_COBERTURA
    return d


def como_fator_de_subregistro(cobertura: pd.DataFrame):
    """Recusa converter a cobertura de jurisdicao em fator de sub-registro.

    A recusa e deliberada. E mais barato falhar do que deixar o numero circular
    com o rotulo errado, como ocorreu na planilha V07, cujo teto de 1,96 vinha da
    razao entre o total de obitos por transporte e a parcela em via publica.

    Raises:
        UsoIndevidoDeCobertura: sempre.
    """
    raise UsoIndevidoDeCobertura(
        "a cobertura de jurisdicao mede a fracao da mortalidade em rodovia "
        "federal, e nao o que a PRF deixou de registrar; o fator de sub-registro "
        "tem outra origem, a ser estabelecida com o local de ocorrencia do SIM"
    )
