"""Ingestao e deduplicacao dos microdados de sinistros da PRF (RF01 a RF04).

O conjunto "todas as causas e tipos" da PRF repete a mesma pessoa uma vez para
cada combinacao de causa e tipo do acidente. Contar linha a linha infla vitimas e
veiculos. Este modulo normaliza o arquivo em quatro tabelas de grao unico:

    ocorrencias  1 linha por acidente          (chave: id)
    veiculos     1 linha por veiculo           (chave: id, id_veiculo)
    pessoas      1 linha por pessoa            (chave: id, pesid)
    causas_tipos 1 linha por causa/tipo        (chave: id, causa_acidente, tipo_acidente)

A informacao de causa e tipo nao se perde: ela sai da tabela de pessoas e vai para
a tabela propria, no grao correto. O vetor C do modelo aditivo do IPEA e contado
sobre pessoas e veiculos, nunca sobre o arquivo bruto.

Contrato (EARS):
- QUANDO um arquivo anual da PRF e lido, o sistema DEVE filtrar pela UF pedida.
- QUANDO as linhas sao normalizadas, o sistema DEVE deduplicar pessoas por
  (id, pesid) e veiculos por (id, id_veiculo).
- SE a coluna pesid estiver ausente, o sistema DEVE falhar de forma explicita, e
  NAO deduplicar por aproximacao.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

# Colunas por grao. O que nao esta aqui pertence a causa/tipo.
COLS_OCORRENCIA = [
    "id", "data_inversa", "dia_semana", "horario", "uf", "br", "km", "municipio",
    "classificacao_acidente", "fase_dia", "sentido_via", "condicao_metereologica",
    "tipo_pista", "tracado_via", "uso_solo", "latitude", "longitude",
    "regional", "delegacia", "uop",
]
COLS_VEICULO = [
    "id", "id_veiculo", "tipo_veiculo", "marca", "ano_fabricacao_veiculo",
]
COLS_PESSOA = [
    "id", "pesid", "id_veiculo", "tipo_envolvido", "estado_fisico", "idade", "sexo",
    # indicadores por pessoa (1 na propria condicao), usados na validacao cruzada
    "ilesos", "feridos_leves", "feridos_graves", "mortos",
]
COLS_CAUSA_TIPO = [
    "id", "causa_principal", "causa_acidente", "ordem_tipo_acidente", "tipo_acidente",
]

# Estado fisico da PRF -> categoria de gravidade do modelo de custo.
GRAVIDADE = {
    "Ileso": "ileso",
    "Lesões Leves": "ferido_leve",
    "Lesoes Leves": "ferido_leve",
    "Lesões Graves": "ferido_grave",
    "Lesoes Graves": "ferido_grave",
    "Óbito": "obito",
    "Obito": "obito",
    "Morto": "obito",
    # Lacuna declarada: a PRF registra a pessoa sem informar o estado fisico.
    # Fica explicita como categoria propria, para nao virar nulo silencioso.
    "Não Informado": "nao_informado",
    "Nao Informado": "nao_informado",
    "Ignorado": "nao_informado",
}


class ColunaObrigatoriaAusente(Exception):
    """Levantada quando o arquivo nao tem a chave necessaria para deduplicar."""


@dataclass
class RelatorioIngestao:
    """Evidencia da ingestao, por ano, para auditoria e para a demo."""
    uf: str
    por_ano: list[dict] = field(default_factory=list)

    def linha(self, **kw) -> None:
        self.por_ano.append(kw)

    def para_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.por_ano)


def _num(serie: pd.Series) -> pd.Series:
    """Converte texto numerico brasileiro (virgula decimal) em float."""
    return pd.to_numeric(
        serie.astype("string").str.replace(",", ".", regex=False), errors="coerce"
    )


def parse_data(serie: pd.Series) -> pd.Series:
    """Converte a data do sinistro sem inferencia, um formato de cada vez.

    A serie da PRF nao e homogenea: 2022 vem em DD/MM/AAAA e os demais anos em
    AAAA-MM-DD. Deixar o pandas inferir descarta silenciosamente as datas cujo dia
    passa de 12 e troca dia por mes nas demais. Cada formato e reconhecido pelo seu
    proprio padrao e convertido de forma explicita.

    Args:
        serie: coluna `data_inversa` como texto.

    Returns:
        Serie de datas, com NaT apenas onde o texto nao casa com formato conhecido.
    """
    s = serie.astype("string").str.strip()
    fora = pd.Series(pd.NaT, index=s.index, dtype="datetime64[ns]")

    iso = s.str.match(r"^\d{4}-\d{2}-\d{2}", na=False)
    fora[iso] = pd.to_datetime(s[iso], format="%Y-%m-%d", errors="coerce")

    br = s.str.match(r"^\d{2}/\d{2}/\d{4}", na=False)
    fora[br] = pd.to_datetime(s[br], format="%d/%m/%Y", errors="coerce")

    return fora


def ler_ano(caminho: Path, uf: str, chunksize: int = 200_000) -> pd.DataFrame:
    """Le um arquivo anual da PRF e devolve apenas as linhas da UF pedida.

    Args:
        caminho: arquivo `acidentes<ano>_todas_causas_tipos.csv`.
        uf: sigla da unidade da federacao.
        chunksize: linhas por bloco, para controlar memoria.

    Returns:
        As linhas brutas da UF, ainda com a repeticao de causa e tipo.

    Raises:
        ColunaObrigatoriaAusente: se faltar `pesid` ou `id_veiculo`.
    """
    blocos = []
    leitor = pd.read_csv(
        caminho, sep=";", encoding="latin-1", dtype=str,
        chunksize=chunksize, on_bad_lines="skip", low_memory=False,
    )
    for bloco in leitor:
        bloco.columns = [c.strip().strip('"') for c in bloco.columns]
        faltando = {"pesid", "id_veiculo", "id"} - set(bloco.columns)
        if faltando:
            raise ColunaObrigatoriaAusente(
                f"{caminho.name}: faltam {sorted(faltando)}; sem elas nao ha deduplicacao segura"
            )
        blocos.append(bloco[bloco["uf"] == uf])
    return pd.concat(blocos, ignore_index=True) if blocos else pd.DataFrame()


def normalizar(bruto: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Separa o arquivo bruto nas quatro tabelas de grao unico.

    Args:
        bruto: linhas de uma UF, com repeticao de causa e tipo.

    Returns:
        Dicionario com ocorrencias, veiculos, pessoas e causas_tipos.
    """
    def sub(cols: list[str], chaves: list[str]) -> pd.DataFrame:
        presentes = [c for c in cols if c in bruto.columns]
        return bruto[presentes].drop_duplicates(subset=chaves).reset_index(drop=True)

    ocorrencias = sub(COLS_OCORRENCIA, ["id"])
    veiculos = sub(COLS_VEICULO, ["id", "id_veiculo"])
    pessoas = sub(COLS_PESSOA, ["id", "pesid"])
    causas = sub(COLS_CAUSA_TIPO, ["id", "causa_acidente", "tipo_acidente"])

    # Tipagem e enriquecimento minimos.
    for c in ("km", "latitude", "longitude"):
        if c in ocorrencias.columns:
            ocorrencias[c] = _num(ocorrencias[c])
    if "br" in ocorrencias.columns:
        ocorrencias["br"] = pd.to_numeric(ocorrencias["br"], errors="coerce").astype("Int64")
    if "data_inversa" in ocorrencias.columns:
        data = parse_data(ocorrencias["data_inversa"])
        ocorrencias["data"] = data
        ocorrencias["ano"] = data.dt.year.astype("Int64")
        ocorrencias["mes"] = data.dt.month.astype("Int64")
    if "idade" in pessoas.columns:
        pessoas["idade"] = pd.to_numeric(pessoas["idade"], errors="coerce").astype("Int64")
    for c in ("ilesos", "feridos_leves", "feridos_graves", "mortos"):
        if c in pessoas.columns:
            pessoas[c] = pd.to_numeric(pessoas[c], errors="coerce").fillna(0).astype("Int64")
    if "estado_fisico" in pessoas.columns:
        pessoas["gravidade"] = pessoas["estado_fisico"].map(GRAVIDADE)

    # Veiculos sem id_veiculo (registro sem veiculo associado) saem da tabela.
    if "id_veiculo" in veiculos.columns:
        veiculos = veiculos[veiculos["id_veiculo"].notna() & (veiculos["id_veiculo"] != "")]

    return {
        "ocorrencias": ocorrencias,
        "veiculos": veiculos,
        "pessoas": pessoas,
        "causas_tipos": causas,
    }


def ingerir(
    origem: Path, uf: str, anos: range | list[int],
    padrao: str = "acidentes{ano}_todas_causas_tipos.csv",
) -> tuple[dict[str, pd.DataFrame], RelatorioIngestao]:
    """Ingere varios anos de uma UF e devolve as tabelas consolidadas.

    Args:
        origem: pasta com os arquivos anuais da PRF.
        uf: unidade da federacao (o parametro de escala).
        anos: anos a processar.
        padrao: nome do arquivo, com {ano}.

    Returns:
        As quatro tabelas concatenadas e o relatorio de ingestao por ano.
    """
    acumulado: dict[str, list[pd.DataFrame]] = {
        "ocorrencias": [], "veiculos": [], "pessoas": [], "causas_tipos": []
    }
    rel = RelatorioIngestao(uf=uf)

    for ano in anos:
        caminho = origem / padrao.format(ano=ano)
        if not caminho.exists():
            rel.linha(ano=ano, arquivo=caminho.name, situacao="ausente")
            continue
        bruto = ler_ano(caminho, uf)
        if bruto.empty:
            rel.linha(ano=ano, arquivo=caminho.name, situacao="sem linhas da UF")
            continue
        tabelas = normalizar(bruto)
        n_bruto = len(bruto)
        n_pessoas = len(tabelas["pessoas"])
        rel.linha(
            ano=ano, arquivo=caminho.name, situacao="ok",
            linhas_brutas=n_bruto,
            ocorrencias=len(tabelas["ocorrencias"]),
            veiculos=len(tabelas["veiculos"]),
            pessoas=n_pessoas,
            reducao_pct=round(100 * (1 - n_pessoas / n_bruto), 1) if n_bruto else 0.0,
        )
        for k, df in tabelas.items():
            acumulado[k].append(df)

    final = {}
    chaves = {
        "ocorrencias": ["id"], "veiculos": ["id", "id_veiculo"],
        "pessoas": ["id", "pesid"], "causas_tipos": ["id", "causa_acidente", "tipo_acidente"],
    }
    for k, partes in acumulado.items():
        if partes:
            df = pd.concat(partes, ignore_index=True)
            presentes = [c for c in chaves[k] if c in df.columns]
            final[k] = df.drop_duplicates(subset=presentes).reset_index(drop=True)
        else:
            final[k] = pd.DataFrame()
    return final, rel


def validar(tabelas: dict[str, pd.DataFrame]) -> list[dict]:
    """Valida a consistencia interna das tabelas normalizadas (RF04).

    Confere se a contagem de pessoas por gravidade bate com os indicadores por
    pessoa do proprio arquivo, se as datas foram todas reconhecidas e se as chaves
    sao unicas. Cada achado sai como um registro, para o relatorio de qualidade.

    Returns:
        Lista de achados, cada um com verificacao, esperado, obtido e situacao.
    """
    achados: list[dict] = []

    def reg(verificacao: str, esperado, obtido) -> None:
        achados.append({
            "verificacao": verificacao, "esperado": esperado, "obtido": obtido,
            "situacao": "ok" if esperado == obtido else "divergencia",
        })

    pes = tabelas.get("pessoas", pd.DataFrame())
    oc = tabelas.get("ocorrencias", pd.DataFrame())

    if not pes.empty and "gravidade" in pes.columns:
        pares = [("obito", "mortos"), ("ferido_grave", "feridos_graves"),
                 ("ferido_leve", "feridos_leves"), ("ileso", "ilesos")]
        for rotulo, indicador in pares:
            if indicador in pes.columns:
                reg(f"pessoas com gravidade '{rotulo}' x soma do indicador '{indicador}'",
                    int((pes["gravidade"] == rotulo).sum()), int(pes[indicador].sum()))
        reg("pessoas com gravidade reconhecida",
            len(pes), int(pes["gravidade"].notna().sum()))
        reg("chave (id, pesid) unica", len(pes), len(pes.drop_duplicates(["id", "pesid"])))

    if not oc.empty:
        if "ano" in oc.columns:
            reg("ocorrencias com data reconhecida", len(oc), int(oc["ano"].notna().sum()))
        reg("chave id unica", len(oc), len(oc.drop_duplicates(["id"])))

    vei = tabelas.get("veiculos", pd.DataFrame())
    if not vei.empty:
        reg("chave (id, id_veiculo) unica", len(vei),
            len(vei.drop_duplicates(["id", "id_veiculo"])))

    return achados


def vetor_c(tabelas: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Monta o vetor C do modelo aditivo do IPEA, por ocorrencia.

    Conta, para cada acidente, as pessoas por gravidade e os veiculos por tipo.
    E a entrada do produto escalar C . M que da o custo do acidente.

    Returns:
        Uma linha por ocorrencia, com as contagens por gravidade e por veiculo.
    """
    oc = tabelas["ocorrencias"][["id"]].copy()

    pes = tabelas["pessoas"]
    if not pes.empty and "gravidade" in pes.columns:
        cont = pes.pivot_table(index="id", columns="gravidade", values="pesid",
                               aggfunc="count", fill_value=0)
        oc = oc.merge(cont, on="id", how="left")

    vei = tabelas["veiculos"]
    if not vei.empty and "tipo_veiculo" in vei.columns:
        contv = vei.pivot_table(index="id", columns="tipo_veiculo", values="id_veiculo",
                                aggfunc="count", fill_value=0)
        contv.columns = [f"veic_{c}" for c in contv.columns]
        oc = oc.merge(contv, on="id", how="left")

    return oc.fillna(0)
