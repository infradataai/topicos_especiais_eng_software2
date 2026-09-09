# Spec (delta) - consulta

## ADDED Requirements

### Requirement: Consulta web direta e interativa
O sistema DEVE (MUST) permitir consultar registros consolidados, fontes e lotes por uma interface web com filtros, ordenacao e paginacao.

#### Scenario: Filtrar registros
- **GIVEN** registros consolidados de mais de um orgao
- **WHEN** o usuario seleciona um orgao e um intervalo de datas na interface web
- **THEN** a pagina exibe somente os registros correspondentes e informa a quantidade retornada

#### Scenario: Consultar a origem
- **GIVEN** um registro exibido na consulta
- **WHEN** o usuario abre seus detalhes
- **THEN** a interface exibe arquivo, orgao, versao, checksum e lote de origem

#### Scenario: Resultado vazio
- **GIVEN** filtros sem registros correspondentes
- **WHEN** a consulta e executada
- **THEN** a interface informa que nao ha resultados e nao apresenta dados de outra consulta

### Requirement: Consulta segura e somente leitura
O sistema DEVE (MUST) rejeitar SQL arbitrario e qualquer operacao de escrita pela interface web.

#### Scenario: Tentativa de SQL arbitrario
- **GIVEN** uma requisicao contendo SQL em vez de filtros permitidos
- **WHEN** a API e chamada
- **THEN** a requisicao e rejeitada sem executar escrita ou consulta fora do contrato
