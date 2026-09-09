# Spec (delta) - relatorios

## ADDED Requirements

### Requirement: Exportacao de relatorio em JSON
O sistema DEVE (MUST) gerar um JSON valido contendo resultados, metricas, alertas, periodo de referencia e metadados de proveniencia.

#### Scenario: Exportar resultado analisado
- **GIVEN** um resultado de qualidade e estatistica associado a uma fonte e versao
- **WHEN** o relatorio JSON e gerado
- **THEN** o arquivo contem as metricas, os alertas e os metadados da fonte, lote e versao

#### Scenario: Resultado sem dados
- **GIVEN** um relatorio sem registros
- **WHEN** o JSON e gerado
- **THEN** o arquivo permanece valido e representa explicitamente a ausencia de registros

### Requirement: Geracao de relatorio em PDF
O sistema DEVE (MUST) gerar um PDF legivel com as mesmas informacoes essenciais do JSON, incluindo titulo, periodo, metricas, alertas e origem.

#### Scenario: Gerar PDF correspondente
- **GIVEN** um relatorio valido
- **WHEN** a exportacao PDF e executada
- **THEN** o arquivo PDF e criado e apresenta as secoes de resumo, qualidade, analise e proveniencia

#### Scenario: Falha de exportacao
- **GIVEN** um relatorio que nao passa na validacao estrutural
- **WHEN** a exportacao e solicitada
- **THEN** a operacao falha com erro descritivo e nao altera os dados consolidados
