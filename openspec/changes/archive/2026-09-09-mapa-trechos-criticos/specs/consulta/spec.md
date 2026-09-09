# Spec (delta) - consulta

## ADDED Requirements

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
