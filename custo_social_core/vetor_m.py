"""Vetor M: custos medios padrao do IPEA, Tabela 1 do TD 2565 (dez/2014).

Este modulo e DADO DE CONFIGURACAO, nao logica. Os valores sao os totais por
componente elementar, transcritos da Tabela 1 do Texto para Discussao 2565
(IPEA, junho de 2020), a precos de dezembro de 2014.

A chave e composta: (componente, gravidade da ocorrencia). A gravidade da
OCORRENCIA seleciona a coluna; a gravidade da VITIMA seleciona a linha. A mesma
vitima leve custa 8.469,44 num acidente com vitimas e 8.635,77 num acidente com
fatalidade.

Parametros fixados no ADR-011.
"""
from __future__ import annotations

# Gravidades da ocorrencia (as tres colunas da Tabela 1)
SEM_VITIMAS = "sem_vitimas"
COM_VITIMAS = "com_vitimas"
COM_FATALIDADE = "com_fatalidade"
GRAVIDADES_OCORRENCIA = (SEM_VITIMAS, COM_VITIMAS, COM_FATALIDADE)

# --- Tabela 1A: componentes associados as pessoas (totais, R$ dez/2014) ---
M_PESSOAS: dict[str, dict[str, float]] = {
    "ileso":        {SEM_VITIMAS:  1_086.14, COM_VITIMAS:   4_110.60, COM_FATALIDADE:   1_839.94},
    "ferido_leve":  {SEM_VITIMAS:  6_456.33, COM_VITIMAS:   8_469.44, COM_FATALIDADE:   8_635.77},
    "ferido_grave": {SEM_VITIMAS: 22_421.06, COM_VITIMAS: 125_133.91, COM_FATALIDADE: 141_155.96},
    "obito":        {SEM_VITIMAS:     199.28, COM_VITIMAS: 335_172.20, COM_FATALIDADE: 433_286.69},
    # Lacuna declarada (ADR-011, decisao 2): entra com custo zero e contagem a parte.
    "nao_informado": {SEM_VITIMAS: 0.0, COM_VITIMAS: 0.0, COM_FATALIDADE: 0.0},
}

# --- Tabela 1B: componentes associados aos veiculos (totais, R$ dez/2014) ---
M_VEICULOS: dict[str, dict[str, float]] = {
    "Automóveis":  {SEM_VITIMAS:  7_159.12, COM_VITIMAS: 12_126.82, COM_FATALIDADE: 19_323.91},
    "Motocicletas": {SEM_VITIMAS: 2_473.21, COM_VITIMAS:  2_741.02, COM_FATALIDADE:  4_269.83},
    "Bicicletas":  {SEM_VITIMAS:      0.00, COM_VITIMAS:    168.74, COM_FATALIDADE:    124.10},
    "Utilitários": {SEM_VITIMAS: 10_569.76, COM_VITIMAS: 20_240.38, COM_FATALIDADE: 35_091.47},
    "Caminhões":   {SEM_VITIMAS: 22_313.92, COM_VITIMAS: 65_656.00, COM_FATALIDADE: 47_825.45},
    "Ônibus":      {SEM_VITIMAS: 16_069.30, COM_VITIMAS: 10_536.86, COM_FATALIDADE: 20_686.09},
    "Outros":      {SEM_VITIMAS: 10_307.36, COM_VITIMAS: 80_108.63, COM_FATALIDADE: 81_209.29},
}

# --- Tabela 1C: institucionais e patrimoniais (uma vez por ocorrencia) ---
M_INSTITUCIONAL: dict[str, float] = {
    SEM_VITIMAS: 453.35, COM_VITIMAS: 338.33, COM_FATALIDADE: 653.06,
}

# --- Mapeamento dos tipos da PRF para as sete classes do IPEA (ADR-011) ---
MAPA_VEICULOS: dict[str, str] = {
    "Automóvel": "Automóveis",
    "Motocicleta": "Motocicletas", "Motoneta": "Motocicletas",
    "Ciclomotor": "Motocicletas", "Triciclo": "Motocicletas",
    "Quadriciclo": "Motocicletas",
    "Bicicleta": "Bicicletas",
    "Caminhonete": "Utilitários", "Camioneta": "Utilitários",
    "Utilitário": "Utilitários",
    "Caminhão": "Caminhões", "Caminhão-trator": "Caminhões",
    "Ônibus": "Ônibus", "Micro-ônibus": "Ônibus",
    "Carroça-charrete": "Outros", "Trator de rodas": "Outros",
    "Motor-casa": "Outros", "Carro de mão": "Outros",
    "Trem-bonde": "Outros", "Outros": "Outros",
}

# Unidades da composicao rodoviaria: nao recebem valor proprio (ADR-011, decisao 3).
UNIDADES_TRATORAS = ("Caminhão", "Caminhão-trator")
UNIDADES_REBOCADAS = ("Semireboque", "Reboque")

# --- Atualizacao monetaria (ADR-011, decisao 1) ---
# Produto dos fatores anuais do IPCA de 2015 a 2026 (2026 parcial ate junho).
# Confere com a aba Parametros da V07: 23.498,77 x 1,884802 = 44.290,53.
DEFLATOR_DEZ2014_JUN2026 = 1.884802
BASE_MONETARIA = "jun/2026"
