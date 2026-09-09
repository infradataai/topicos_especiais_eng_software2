# consulta Specification

## Purpose

Permitir a consulta web direta, paginada e somente leitura dos registros consolidados e de sua proveniência.

## Requirements

### Requirement: Consulta web direta e interativa
O sistema DEVE (MUST) permitir consultar registros consolidados, fontes e lotes por uma interface web com filtros, ordenação e paginação.

#### Scenario: Filtrar registros
- **GIVEN** registros consolidados de mais de um órgão
- **WHEN** o usuário seleciona um órgão e um intervalo de datas na interface web
- **THEN** a página exibe somente os registros correspondentes e informa a quantidade retornada

#### Scenario: Consultar a origem
- **GIVEN** um registro exibido na consulta
- **WHEN** o usuário abre seus detalhes
- **THEN** a interface exibe arquivo, órgão, versão, checksum e lote de origem

#### Scenario: Resultado vazio
- **GIVEN** filtros sem registros correspondentes
- **WHEN** a consulta é executada
- **THEN** a interface informa que não há resultados e não apresenta dados de outra consulta

### Requirement: Consulta segura e somente leitura
O sistema DEVE (MUST) rejeitar SQL arbitrário e qualquer operação de escrita pela interface web.

#### Scenario: Tentativa de SQL arbitrário
- **GIVEN** uma requisição contendo SQL em vez de filtros permitidos
- **WHEN** a API é chamada
- **THEN** a requisição é rejeitada sem executar escrita ou consulta fora do contrato
