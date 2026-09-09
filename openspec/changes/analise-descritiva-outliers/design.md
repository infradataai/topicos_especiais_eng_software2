# Design - Analise descritiva e deteccao de outliers

## Decisoes

A funcao recebe uma coluna numerica da tabela consolidada e devolve um relatorio serializavel. Valores ausentes ou nao numericos sao contabilizados como invalidos e nao entram nas metricas. O desvio padrao deve declarar se usa a definicao amostral ou populacional; este contrato usa a definicao amostral.

Outliers sao observacoes abaixo de Q1 - 1,5 vezes o IQR ou acima de Q3 + 1,5 vezes o IQR. A analise e somente leitura.

## Interface

`analisar_coluna(con, tabela, coluna) -> dict`, contendo `n_validos`, `n_invalidos`, `media`, `mediana`, `desvio_padrao`, quartis, limites e identificadores das observacoes sinalizadas.
