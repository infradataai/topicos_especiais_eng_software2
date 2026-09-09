"""Configuracao do nucleo: a UF e o unico parametro que troca entre piloto e escala.

Rodar o piloto RN e rodar o Brasil diferem por UF e pela camada fina abaixo
(corredores e extensao do mapa). O modelo de custo, o referenciamento e a
criticidade nao mudam.
"""
from __future__ import annotations

# --- Parametro de escala (o unico que troca) ---
UF: str = "RN"

# --- Camada fina especifica da UF (so configuracao, nao logica) ---
# Corredores locais destacados no mapa do piloto. Para o Brasil, a lista vazia
# significa "todos os segmentos da UF", sem corredor em destaque.
CORREDORES_POR_UF: dict[str, list[int]] = {
    "RN": [101, 304, 226, 406],  # BRs que estruturam a malha federal do RN
}

# --- Categorias de gravidade do custo refinado (item 1 do escopo) ---
# A base do Ipea tem 3 classes por ocorrencia; o refino separa feridos em
# leve e grave, chegando a 4 categorias ancoradas em vitima.
CATEGORIAS: tuple[str, ...] = ("sem_feridos", "ferido_leve", "ferido_grave", "obito")

# --- Ancora Ipea por ocorrencia, TD 2565, corrigida para jun/2026 (R$) ---
# Fonte: Custo_Social_Parametros_e_Resultados_V07.xlsx, aba Parametros.
# Valores de ancora e validacao; o refino decompoe a classe "com_feridos".
CUSTO_IPEA_OCORRENCIA: dict[str, float] = {
    "sem_vitimas": 44290.53,
    "com_feridos": 182350.42,
    "com_vitima_fatal": 1253056.76,
}

# --- Cenarios de correcao de subregistro (item 5), aba Correcao_Subregistro ---
# Fator aplicado sobre a contagem observada da PRF para aproximar o SIM.
FATOR_SUBREGISTRO: dict[str, float] = {
    "piso": 1.0,      # PRF como esta
    "central": 1.4,
    "teto": 1.96,
}

CENARIO_SUBREGISTRO_PADRAO: str = "central"

# Dias do ano usados para converter VMDa em veiculos-km anuais na exposicao.
DIAS_ANO: int = 365
