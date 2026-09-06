# Spec (delta) — lai-loader

## ADDED Requirements

### Requirement: Carga de CSV para a camada bronze
O sistema DEVE ler um arquivo CSV de microdados como texto (dtype str) e carregá-lo em uma tabela SQLite informada.

#### Scenario: Carregar um arquivo novo
- **GIVEN** um CSV com as colunas obrigatórias e duas linhas de dados
- **WHEN** o carregador é executado sobre uma tabela inexistente
- **THEN** a tabela é criada e passa a conter duas linhas

#### Scenario: Recarregar sem duplicar (idempotência)
- **GIVEN** um CSV já carregado uma vez
- **WHEN** o carregador é executado de novo sobre o mesmo arquivo e tabela
- **THEN** nenhuma linha nova é inserida e a contagem permanece a mesma

### Requirement: Validação de colunas obrigatórias
O sistema DEVE recusar o arquivo quando faltar qualquer coluna obrigatória.

#### Scenario: Coluna obrigatória ausente (caso de borda)
- **GIVEN** um CSV sem uma das colunas obrigatórias
- **WHEN** o carregador é executado
- **THEN** uma exceção de colunas ausentes é levantada e nada é gravado

#### Scenario: Arquivo só com cabeçalho
- **GIVEN** um CSV com cabeçalho válido e nenhuma linha de dados
- **WHEN** o carregador é executado
- **THEN** o retorno é zero e a tabela não recebe linhas
