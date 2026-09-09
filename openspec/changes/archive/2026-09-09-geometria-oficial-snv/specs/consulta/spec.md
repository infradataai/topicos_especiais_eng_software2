# Spec (delta) - consulta

## ADDED Requirements

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
