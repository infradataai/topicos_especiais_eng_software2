# snv-referenciamento Specification

## Purpose

Ancorar cada ocorrência ao segmento do Sistema Nacional de Viação correspondente ao ano do sinistro, com o critério de desempate declarado.

## Requirements

### Requirement: Leitura da planilha do SNV
O sistema DEVE ler a planilha de uma safra do SNV reconhecendo o cabeçalho na terceira linha, e DEVE expor ao menos as colunas de BR, unidade da federação, código do segmento, quilômetro inicial, quilômetro final, extensão, administração e jurisdição.

#### Scenario: Ler uma safra e recuperar os segmentos de uma UF
- **GIVEN** a planilha da safra `202501A`
- **WHEN** a leitura é executada para a sigla `RN`
- **THEN** são devolvidos os segmentos daquele estado, com as colunas obrigatórias preenchidas

#### Scenario: Planilha sem o cabeçalho esperado (caso de borda)
- **GIVEN** uma planilha em que a terceira linha não traz os rótulos de coluna esperados
- **WHEN** a leitura é executada
- **THEN** uma exceção de cabeçalho não reconhecido é levantada, e o sistema NÃO adivinha a posição das colunas

### Requirement: Seleção da safra vigente no ano do sinistro
O sistema DEVE ancorar cada sinistro na safra do SNV vigente no ano em que ele ocorreu, entendida como a safra mais recente cujo ano de referência não ultrapassa o ano do sinistro.

#### Scenario: Sinistro de um ano com safra própria
- **GIVEN** as safras `201811A`, `202001A` e `202501A`
- **WHEN** um sinistro de 2020 é ancorado
- **THEN** a safra usada é `202001A`

#### Scenario: Sinistro anterior à primeira safra disponível (caso de borda)
- **GIVEN** apenas a safra `202001A`
- **WHEN** um sinistro de 2019 é ancorado
- **THEN** uma exceção de safra indisponível é levantada, e o sistema NÃO usa uma safra posterior ao sinistro

### Requirement: Ancoragem por referenciamento linear
O sistema DEVE ancorar a ocorrência ao segmento cuja faixa de quilometragem contém o quilômetro do sinistro, na mesma rodovia e unidade da federação.

#### Scenario: Quilômetro dentro da faixa de um segmento
- **GIVEN** um segmento da BR-101 no RN, de 6,1 a 20,4 quilômetros
- **WHEN** um sinistro da BR-101 no RN, no quilômetro 12,5, é ancorado
- **THEN** ele é atribuído a esse segmento

#### Scenario: Quilômetro fora de qualquer faixa (caso de borda)
- **GIVEN** os segmentos da BR-101 no RN, que terminam no quilômetro 320
- **WHEN** um sinistro é registrado no quilômetro 400 da mesma rodovia
- **THEN** a ocorrência é marcada como não ancorada, com o motivo registrado
- **AND** o sistema NÃO a atribui ao segmento mais próximo

### Requirement: Desempate de trechos coincidentes
Quando mais de um segmento contiver o mesmo quilômetro, caso dos trechos coincidentes em que a via física recebe mais de uma designação, o sistema DEVE atribuir a ocorrência a um único segmento, pela ordem de preferência: a jurisdição federal; entre essas, o tipo de trecho eixo principal; entre esses, o de menor extensão; e, persistindo o empate, o de menor código. A escolha DEVE ser registrada como desempate.

A jurisdição federal vem primeiro porque a base de sinistros da PRF cobre a malha federal. Ancorar uma ocorrência da PRF num trecho estadual coincidente atribuiria custo federal a via estadual e contaminaria a comparação entre os regimes DNIT e ANTT.

#### Scenario: Dois segmentos contêm o mesmo quilômetro (caso de borda)
- **GIVEN** dois segmentos da mesma rodovia e UF cujas faixas se sobrepõem no quilômetro 50
- **WHEN** um sinistro nesse quilômetro é ancorado
- **THEN** a ocorrência é atribuída a exatamente um segmento
- **AND** o resultado indica que houve desempate por coincidência

#### Scenario: Trecho federal e trecho estadual coincidentes (caso de borda)
- **GIVEN** um segmento de jurisdição federal e outro de jurisdição estadual, ambos contendo o quilômetro 50, sendo o estadual de menor extensão
- **WHEN** um sinistro da PRF nesse quilômetro é ancorado
- **THEN** a ocorrência é atribuída ao segmento federal, apesar de o estadual ser mais curto

### Requirement: Regime de administração do segmento
O sistema DEVE derivar o regime de cada segmento da coluna de administração do SNV, classificando como DNIT a administração federal e como ANTT a concessão federal. As demais administrações DEVEM receber o rótulo próprio, sem serem forçadas a um dos dois regimes.

#### Scenario: Segmento sob administração federal
- **GIVEN** um segmento cuja administração é `Federal`
- **WHEN** o regime é derivado
- **THEN** o regime é `DNIT`

#### Scenario: Segmento sob concessão
- **GIVEN** um segmento cuja administração é `Concessão Federal`
- **WHEN** o regime é derivado
- **THEN** o regime é `ANTT`

#### Scenario: Administração fora dos dois regimes
- **GIVEN** um segmento cuja administração é `Estadual`
- **WHEN** o regime é derivado
- **THEN** o regime é `outro`, e a ocorrência NÃO entra na comparação entre DNIT e ANTT

### Requirement: Agregação do custo por segmento
O sistema DEVE somar, por segmento, o custo social das ocorrências ancoradas nele, e DEVE devolver também a extensão do segmento, para permitir o custo por quilômetro.

O segmento DEVE aparecer uma única vez no resultado, ainda que tenha sido ancorado em mais de uma safra. O custo soma as ocorrências de todas as safras, e a extensão é a da safra mais recente em que o segmento foi ancorado. Repetir o segmento por safra somaria a mesma extensão física várias vezes e inflaria a malha do estado.

#### Scenario: Somar duas ocorrências no mesmo segmento
- **GIVEN** duas ocorrências ancoradas no mesmo segmento, com custos de R$ 100.000,00 e R$ 300.000,00
- **WHEN** a agregação é executada
- **THEN** o custo do segmento é R$ 400.000,00
- **AND** o custo por quilômetro é esse total dividido pela extensão do segmento

#### Scenario: Segmento ancorado em duas safras com extensão diferente (caso de borda)
- **GIVEN** um segmento ancorado na safra `202310A` com extensão 10,0 km e na safra `202511A` com extensão 12,0 km
- **WHEN** a agregação é executada
- **THEN** o segmento aparece uma única vez
- **AND** a extensão adotada é 12,0 km, da safra mais recente
- **AND** o custo soma as ocorrências das duas safras
