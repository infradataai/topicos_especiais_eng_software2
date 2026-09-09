# analise Specification

## Purpose

Resumir variáveis numéricas consolidadas e sinalizar observações potencialmente anormais de forma reproduzível e somente leitura.

## Requirements

### Requirement: Estatística descritiva
O sistema DEVE (MUST) calcular média, mediana e desvio padrão amostral para uma coluna numérica consolidada, informando também a quantidade de valores válidos e inválidos.

#### Scenario: Coluna numérica válida
- **GIVEN** uma coluna com os valores 10, 20 e 30
- **WHEN** a análise é executada
- **THEN** o relatório informa média 20, mediana 20 e desvio padrão amostral calculado sobre os três valores

#### Scenario: Valores inválidos
- **GIVEN** uma coluna com valores numéricos, vazios e texto
- **WHEN** a análise é executada
- **THEN** vazios e textos são contados como inválidos e ficam fora das métricas

### Requirement: Detecção automática de outliers
O sistema DEVE (MUST) sinalizar automaticamente observações fora dos limites de 1,5 vezes o IQR e não DEVE remover nem alterar essas observações.

#### Scenario: Observação fora do limite IQR
- **GIVEN** uma coluna numérica com uma observação acima do limite superior do IQR
- **WHEN** a análise é executada
- **THEN** essa observação é listada como outlier com seu valor e identificador

#### Scenario: Sem outliers
- **GIVEN** uma coluna numérica cujos valores estão dentro dos limites IQR
- **WHEN** a análise é executada
- **THEN** a lista de outliers fica vazia e os dados permanecem inalterados
