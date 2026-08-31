# Spec (delta) — lai-pdf

## ADDED Requirements

### Requirement: Normalização de linhas extraídas
O sistema DEVE converter as linhas brutas de uma tabela em registros, usando a primeira linha como cabeçalho.

#### Scenario: Tabela com cabeçalho e dados
- **GIVEN** linhas com um cabeçalho e duas linhas de dados
- **WHEN** a normalização é aplicada
- **THEN** são devolvidos dois registros com as chaves do cabeçalho

#### Scenario: Linhas em branco no meio da tabela (caso de borda)
- **GIVEN** linhas em que uma delas está inteiramente vazia
- **WHEN** a normalização é aplicada
- **THEN** a linha vazia é descartada e não vira registro

#### Scenario: Célula faltante na linha de dados
- **GIVEN** uma linha de dados com menos células que o cabeçalho
- **WHEN** a normalização é aplicada
- **THEN** as células faltantes são preenchidas com vazio

### Requirement: Recusa de PDF sem tabela útil
O sistema DEVE sinalizar quando não houver cabeçalho e ao menos uma linha de dados.

#### Scenario: Tabela sem linhas de dados
- **GIVEN** apenas a linha de cabeçalho
- **WHEN** a normalização é aplicada
- **THEN** uma exceção de tabela vazia é levantada
