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

### Requirement: Consulta de segmentos críticos
O sistema DEVE expor os segmentos do SNV com ocorrência ancorada, uma linha por segmento,
trazendo extensão, custo social agregado, número de ocorrências, volume médio diário anual
e as duas leituras de criticidade: custo por quilômetro e custo por veículo-quilômetro.

#### Scenario: Ranque nas duas leituras
- **GIVEN** um banco com segmentos ancorados e exposição carregada
- **WHEN** a consulta de segmentos é executada para uma unidade da federação
- **THEN** cada linha traz as duas leituras de criticidade, e a ordenação pode usar qualquer uma delas

#### Scenario: Segmento presente em várias safras
- **GIVEN** um segmento cujo código aparece em mais de uma safra do SNV
- **WHEN** a consulta agrega o custo do segmento
- **THEN** o custo é contado uma vez, e a extensão vem da safra mais recente

#### Scenario: Segmento sem volume medido
- **GIVEN** um segmento sem posto de contagem no PNCT
- **WHEN** a consulta devolve a linha do segmento
- **THEN** a leitura por veículo-quilômetro é nula e a leitura por quilômetro permanece

### Requirement: Consulta de ocorrências com coordenada
O sistema DEVE expor as ocorrências de uma unidade da federação com latitude, longitude,
BR, quilômetro, ano, categoria e custo social, de forma paginada, para alimentar o mapa.

#### Scenario: Ocorrências de um trecho
- **GIVEN** um banco com ocorrências ancoradas e custo calculado
- **WHEN** a consulta é filtrada por unidade da federação e BR
- **THEN** cada item traz coordenada e custo, e o total acompanha a página

### Requirement: Recusa em banco sem as tabelas de sinistro
O sistema DEVE verificar a presença das tabelas do núcleo antes de consultá-las e DEVE
responder com erro de requisição e mensagem explícita quando elas não existirem, sem
deixar vazar o erro do banco.

#### Scenario: Banco apenas com o esquema da LAI
- **GIVEN** um banco que contém apenas `fontes`, `lotes` e `registros_canonicos`
- **WHEN** a rota de segmentos é chamada
- **THEN** a resposta é 400 e informa que o banco não tem as tabelas de sinistro

### Requirement: Página de mapa dos trechos críticos
O sistema DEVE servir uma página que projeta as ocorrências sobre mapa e lista os
segmentos ordenados por criticidade, permitindo alternar entre as duas leituras.

#### Scenario: Página servida
- **GIVEN** a aplicação em execução
- **WHEN** a rota do mapa é requisitada
- **THEN** a resposta é HTML e contém o contêiner do mapa e a tabela de segmentos

### Requirement: Traçado oficial do segmento no mapa
O sistema DEVE devolver, para cada segmento, o traçado oficial da via a partir da
base geométrica do SNV, casada pelo código do segmento, quando essa geometria
estiver disponível no banco.

#### Scenario: Segmento com geometria oficial
- **GIVEN** um banco com a tabela de geometria populada para a unidade da federação
- **WHEN** a geometria dos segmentos é consultada
- **THEN** o traçado devolvido é o oficial, e a fonte é declarada como SNV do DNIT

#### Scenario: Recuo para a aproximação por sinistros
- **GIVEN** um segmento sem geometria oficial no banco
- **WHEN** a geometria dos segmentos é consultada
- **THEN** o traçado devolvido é a ligação dos sinistros por quilômetro, e a fonte é declarada como aproximação

### Requirement: Ingestão da base geométrica do SNV
O sistema DEVE ler a base geométrica do SNV no formato shapefile, filtrar a unidade
da federação, simplificar cada traçado e gravar o resultado na tabela de geometria,
com o código, a safra e a lista de pontos.

#### Scenario: Ingestão de uma safra
- **GIVEN** um shapefile do SNV com segmentos de mais de uma unidade da federação
- **WHEN** a ingestão é executada para uma unidade da federação e uma safra
- **THEN** apenas os segmentos daquela unidade são gravados, com os pontos simplificados
