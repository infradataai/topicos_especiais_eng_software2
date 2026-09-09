# Spec (delta) — exposicao

## ADDED Requirements

### Requirement: Leitura do arquivo anual do VMDa
O sistema DEVE ler o arquivo anual do Plano Nacional de Contagem de Tráfego identificando a aba de dados por conteúdo, e NÃO por nome fixo. A aba de dados é a que não se chama Metadados; havendo mais de uma, o sistema DEVE recusar em vez de escolher.

#### Scenario: Aba de dados com nome variável entre anos
- **GIVEN** um arquivo cuja aba de dados se chama `VMDa2025_SNV202401A`
- **WHEN** a leitura é executada
- **THEN** a aba é reconhecida e os dados são devolvidos

#### Scenario: Arquivo sem aba de dados (caso de borda)
- **GIVEN** um arquivo que contém apenas a aba `Metadados`
- **WHEN** a leitura é executada
- **THEN** uma exceção de aba de dados ausente é levantada

### Requirement: Volume médio diário nos dois sentidos
O sistema DEVE somar o volume dos dois sentidos para obter o tráfego total do segmento. Quando um dos sentidos estiver ausente, o presente DEVE ser usado, e o resultado DEVE registrar que o sentido faltou.

#### Scenario: Segmento com os dois sentidos preenchidos
- **GIVEN** um segmento com volume de 701 no sentido crescente e 796 no decrescente
- **WHEN** o tráfego total é calculado
- **THEN** o resultado é 1.497

#### Scenario: Segmento com um sentido ausente (caso de borda)
- **GIVEN** um segmento com volume de 701 no sentido crescente e nenhum valor no decrescente
- **WHEN** o tráfego total é calculado
- **THEN** o resultado é 701, e o registro indica sentido incompleto

#### Scenario: Segmento sem nenhuma medição
- **GIVEN** um segmento sem valor em nenhum dos dois sentidos
- **WHEN** o tráfego total é calculado
- **THEN** o resultado é nulo declarado, e o segmento NÃO recebe exposição imputada em silêncio

### Requirement: Agregação de múltiplos postos no mesmo segmento
Quando o mesmo código de segmento aparecer mais de uma vez, o que ocorre por haver mais de um posto de contagem no trecho, o sistema DEVE agregar pela média dos volumes e DEVE registrar quantos postos foram agregados.

#### Scenario: Segmento com dois postos de contagem (caso de borda)
- **GIVEN** o mesmo código com tráfego total de 1.497 num posto e 1.724 noutro
- **WHEN** a agregação é executada
- **THEN** o volume do segmento é 1.610,5
- **AND** o registro indica dois postos agregados

### Requirement: Exposição anual em veículos-quilômetro
O sistema DEVE calcular a exposição anual do segmento como o produto do volume médio diário, da extensão em quilômetros e do número de dias do ano.

#### Scenario: Calcular a exposição de um segmento
- **GIVEN** um segmento de 14,3 km com volume médio diário de 1.497 veículos
- **WHEN** a exposição anual é calculada
- **THEN** o resultado é 1.497 × 14,3 × 365 veículos-quilômetro

### Requirement: Criticidade por exposição
O sistema DEVE calcular o custo social por veículo-quilômetro de cada segmento, e DEVE devolver as duas leituras lado a lado: o custo por quilômetro e o custo por exposição.

#### Scenario: Trecho movimentado e trecho vazio com o mesmo custo
- **GIVEN** dois segmentos de mesma extensão e mesmo custo social, um com volume de 20.000 e outro com volume de 2.000
- **WHEN** a criticidade por exposição é calculada
- **THEN** o segmento de menor volume tem criticidade dez vezes maior

#### Scenario: Segmento sem exposição conhecida (caso de borda)
- **GIVEN** um segmento com custo social e sem volume medido
- **WHEN** a criticidade por exposição é calculada
- **THEN** o valor é nulo declarado, e o segmento aparece no resultado marcado como sem exposição
- **AND** o sistema NÃO o exclui do ranque por custo por quilômetro
