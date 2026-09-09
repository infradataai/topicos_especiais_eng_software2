# Spec (delta) - analise

## ADDED Requirements

### Requirement: Estatistica descritiva
O sistema DEVE (MUST) calcular media, mediana e desvio padrao amostral para uma coluna numerica consolidada, informando tambem a quantidade de valores validos e invalidos.

#### Scenario: Coluna numerica valida
- **GIVEN** uma coluna com os valores 10, 20 e 30
- **WHEN** a analise e executada
- **THEN** o relatorio informa media 20, mediana 20 e desvio padrao amostral calculado sobre os tres valores

#### Scenario: Valores invalidos
- **GIVEN** uma coluna com valores numericos, vazios e texto
- **WHEN** a analise e executada
- **THEN** vazios e textos sao contados como invalidos e ficam fora das metricas

### Requirement: Deteccao automatica de outliers
O sistema DEVE (MUST) sinalizar automaticamente observacoes fora dos limites de 1,5 vezes o IQR e nao DEVE remover nem alterar essas observacoes.

#### Scenario: Observacao fora do limite IQR
- **GIVEN** uma coluna numerica com uma observacao acima do limite superior do IQR
- **WHEN** a analise e executada
- **THEN** essa observacao e listada como outlier com seu valor e identificador

#### Scenario: Sem outliers
- **GIVEN** uma coluna numerica cujos valores estao dentro dos limites IQR
- **WHEN** a analise e executada
- **THEN** a lista de outliers fica vazia e os dados permanecem inalterados
