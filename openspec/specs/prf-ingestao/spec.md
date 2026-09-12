# prf-ingestao Specification

## Purpose

Ler os arquivos anuais de sinistros da Polícia Rodoviária Federal e devolvê-los em quatro tabelas de grão único, de forma determinística e auditável.

## Requirements

### Requirement: Leitura do arquivo anual por unidade da federação
O sistema DEVE ler um arquivo anual de sinistros da PRF e devolver apenas as linhas da unidade da federação informada. A unidade da federação é parâmetro, e o mesmo código serve ao piloto e à escala nacional.

#### Scenario: Filtrar as linhas de uma UF
- **GIVEN** um arquivo anual com linhas de várias unidades da federação
- **WHEN** a leitura é executada com a sigla `RN`
- **THEN** apenas as linhas cuja coluna `uf` é `RN` são devolvidas

#### Scenario: Chave de deduplicação ausente (caso de borda)
- **GIVEN** um arquivo sem a coluna `pesid` ou sem `id_veiculo`
- **WHEN** a leitura é executada
- **THEN** uma exceção de coluna obrigatória ausente é levantada, e o sistema NÃO deduplica por aproximação

### Requirement: Normalização em tabelas de grão único
O sistema DEVE separar as linhas brutas em quatro tabelas, cada uma com um grão e uma chave próprios: ocorrências por `id`, veículos por `(id, id_veiculo)`, pessoas por `(id, pesid)` e pares de causa e tipo por `(id, causa_acidente, tipo_acidente)`.

#### Scenario: Deduplicar pessoas e veículos repetidos por causa e tipo
- **GIVEN** um acidente com duas pessoas e dois veículos, repetido em duas combinações de causa e tipo, totalizando quatro linhas
- **WHEN** a normalização é executada
- **THEN** resultam uma ocorrência, duas pessoas e dois veículos

#### Scenario: Preservar a causa e o tipo no grão correto
- **GIVEN** o mesmo acidente com duas combinações de causa e tipo
- **WHEN** a normalização é executada
- **THEN** a tabela de causas e tipos contém as duas combinações, e nenhuma informação é descartada

### Requirement: Reconhecimento determinístico da data
O sistema DEVE converter a data do sinistro reconhecendo cada formato pelo seu próprio padrão, sem inferência automática. Os formatos aceitos são `AAAA-MM-DD` e `DD/MM/AAAA`.

#### Scenario: Série com formatos mistos entre anos
- **GIVEN** as datas `2019-01-01`, `01/01/2022`, `25/12/2022` e `2024-07-09`
- **WHEN** a conversão é executada
- **THEN** os anos resultantes são 2019, 2022, 2022 e 2024, e os meses são 1, 1, 12 e 7

#### Scenario: Dia acima de doze no formato brasileiro (caso de borda)
- **GIVEN** a data `31/03/2022`, que a inferência automática descartaria
- **WHEN** a conversão é executada
- **THEN** a data é reconhecida, com mês 3 e dia 31

#### Scenario: Texto fora de qualquer formato conhecido
- **GIVEN** um texto que não casa com nenhum dos formatos aceitos
- **WHEN** a conversão é executada
- **THEN** o resultado é nulo declarado, e o validador contabiliza a perda

### Requirement: Classificação explícita da gravidade
O sistema DEVE mapear o estado físico da pessoa para as categorias `ileso`, `ferido_leve`, `ferido_grave` e `obito`. A ausência de informação DEVE virar a categoria `nao_informado`, e NÃO um valor nulo.

#### Scenario: Mapear as quatro categorias de gravidade
- **GIVEN** pessoas com estado físico `Óbito` e `Lesões Leves`
- **WHEN** a normalização é executada
- **THEN** as gravidades resultantes são `obito` e `ferido_leve`

#### Scenario: Estado físico não informado
- **GIVEN** uma pessoa com estado físico `Não Informado`
- **WHEN** a normalização é executada
- **THEN** a gravidade é `nao_informado` e nenhuma gravidade fica nula

### Requirement: Validação cruzada de consistência
O sistema DEVE conferir a contagem de pessoas por gravidade contra os indicadores por pessoa do próprio arquivo, a unicidade das chaves de cada grão e o reconhecimento das datas, e DEVE devolver cada achado com situação `ok` ou `divergencia`.

#### Scenario: Contagem por gravidade confere com o indicador do arquivo
- **GIVEN** um conjunto normalizado com um óbito
- **WHEN** a validação é executada
- **THEN** a verificação da gravidade `obito` contra a soma do indicador `mortos` resulta `ok`

#### Scenario: Chave duplicada é acusada
- **GIVEN** uma tabela de pessoas com uma linha repetida na chave `(id, pesid)`
- **WHEN** a validação é executada
- **THEN** a verificação de unicidade dessa chave resulta `divergencia`

### Requirement: Montagem do vetor C
O sistema DEVE produzir, por ocorrência, a contagem de pessoas por gravidade e de veículos por tipo, no formato que o modelo aditivo do IPEA consome.

#### Scenario: Contar pessoas e veículos de uma ocorrência
- **GIVEN** um acidente com um óbito, um ferido leve, uma motocicleta e um automóvel
- **WHEN** o vetor C é montado
- **THEN** a linha da ocorrência traz 1 em `obito`, 1 em `ferido_leve`, 1 em `veic_Motocicleta` e 1 em `veic_Automóvel`
