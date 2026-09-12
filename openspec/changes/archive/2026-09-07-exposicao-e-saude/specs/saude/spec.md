# Spec (delta) — saude

## ADDED Requirements

### Requirement: Leitura dos agregados do DATASUS
O sistema DEVE ler os arquivos agregados do DATASUS reconhecendo a marca de ordem de byte no início do cabeçalho, de modo que o nome da primeira coluna não carregue caractere invisível.

#### Scenario: Arquivo com marca de ordem de byte (caso de borda)
- **GIVEN** um arquivo cujo cabeçalho começa com a marca de ordem de byte antes de `uf`
- **WHEN** a leitura é executada
- **THEN** a primeira coluna se chama `uf`, sem caractere invisível

### Requirement: Óbitos por acidente de transporte
O sistema DEVE carregar os óbitos por acidente de transporte por unidade da federação e ano, com a abertura entre óbito em estabelecimento de saúde e óbito em via pública.

#### Scenario: Consultar os óbitos de uma UF num ano
- **GIVEN** o agregado do SIM carregado
- **WHEN** os óbitos do `RN` em 2024 são consultados
- **THEN** o total, a parcela em estabelecimento de saúde e a parcela em via pública são devolvidos

### Requirement: Internações por causa externa
O sistema DEVE carregar as internações por acidente de transporte por unidade da federação, ano e mês, como lastro da completude do registro de ferido grave.

#### Scenario: Agregar internações do ano
- **GIVEN** o agregado do SIH com doze meses de uma unidade da federação
- **WHEN** o total do ano é consultado
- **THEN** o resultado é a soma dos doze meses

### Requirement: Cobertura da PRF sobre o SIM
O sistema DEVE calcular a razão entre os óbitos registrados pela PRF e os óbitos por transporte do SIM, por unidade da federação e ano, e DEVE rotular essa razão como cobertura de jurisdição, e NÃO como subregistro.

A distinção é de método. A PRF cobre a malha federal, e o SIM cobre todas as vias. A razão entre os dois mede quanto da mortalidade de trânsito ocorre em rodovia federal, e usá-la como fator de subregistro multiplicaria o custo federal por um fator que descreve jurisdição.

#### Scenario: Calcular a cobertura de uma UF
- **GIVEN** 118 óbitos da PRF e 509 óbitos por transporte do SIM no `RN` em 2024
- **WHEN** a cobertura é calculada
- **THEN** o resultado é 23,2%
- **AND** o resultado é rotulado como cobertura de jurisdição

#### Scenario: Recusar o uso como fator de subregistro (caso de borda)
- **GIVEN** a cobertura de jurisdição de uma unidade da federação
- **WHEN** ela é solicitada como fator de correção de subregistro
- **THEN** o sistema recusa, e a mensagem indica que o fator de subregistro tem outra origem
