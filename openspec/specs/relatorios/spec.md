# relatorios Specification

## Purpose

Exportar resultados de qualidade, estatística, alertas e proveniência em formatos estruturados para integração e leitura humana.

## Requirements

### Requirement: Exportação de relatório em JSON
O sistema DEVE (MUST) gerar um JSON válido contendo resultados, métricas, alertas, período de referência e metadados de proveniência.

#### Scenario: Exportar resultado analisado
- **GIVEN** um resultado de qualidade e estatística associado a uma fonte e versão
- **WHEN** o relatório JSON é gerado
- **THEN** o arquivo contém as métricas, os alertas e os metadados da fonte, lote e versão

#### Scenario: Resultado sem dados
- **GIVEN** um relatório sem registros
- **WHEN** o JSON é gerado
- **THEN** o arquivo permanece válido e representa explicitamente a ausência de registros

### Requirement: Geração de relatório em PDF
O sistema DEVE (MUST) gerar um PDF legível com as mesmas informações essenciais do JSON, incluindo título, período, métricas, alertas e origem.

#### Scenario: Gerar PDF correspondente
- **GIVEN** um relatório válido
- **WHEN** a exportação PDF é executada
- **THEN** o arquivo PDF é criado e apresenta as seções de resumo, qualidade, análise e proveniência

#### Scenario: Falha de exportação
- **GIVEN** um relatório que não passa na validação estrutural
- **WHEN** a exportação é solicitada
- **THEN** a operação falha com erro descritivo e não altera os dados consolidados
