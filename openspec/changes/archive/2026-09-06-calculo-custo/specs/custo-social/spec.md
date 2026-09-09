# Spec (delta) — custo-social

## ADDED Requirements

### Requirement: Seleção da coluna do vetor M pela gravidade da ocorrência
O sistema DEVE escolher a coluna do vetor M pela classificação do acidente, entre sem vítimas, com vítimas e com fatalidade. A gravidade da vítima seleciona a linha; a gravidade da ocorrência seleciona a coluna.

#### Scenario: Mesma vítima em ocorrências de gravidade diferente
- **GIVEN** uma vítima de lesão leve
- **WHEN** ela está numa ocorrência com vítimas feridas
- **THEN** o custo aplicado é R$ 8.469,44, a preços de dezembro de 2014
- **AND** quando a mesma vítima está numa ocorrência com fatalidade, o custo aplicado é R$ 8.635,77

#### Scenario: Classificação de acidente desconhecida (caso de borda)
- **GIVEN** uma ocorrência cuja classificação não é nenhuma das três previstas
- **WHEN** o cálculo é executado
- **THEN** uma exceção de classificação desconhecida é levantada, e o sistema NÃO adota uma coluna por omissão

### Requirement: Custo associado às pessoas
O sistema DEVE somar, para cada gravidade de vítima, a contagem de pessoas multiplicada pelo total da Tabela 1A na coluna da ocorrência.

#### Scenario: Somar pessoas de gravidades distintas
- **GIVEN** uma ocorrência com fatalidade, com dois mortos e um ileso
- **WHEN** o custo das pessoas é calculado
- **THEN** o subtotal é 2 × 433.286,69 mais 1 × 1.839,94, igual a R$ 868.413,32

#### Scenario: Gravidade não informada não soma custo
- **GIVEN** uma ocorrência com uma vítima leve e duas pessoas sem estado físico informado
- **WHEN** o custo das pessoas é calculado
- **THEN** apenas a vítima leve soma custo
- **AND** o resultado declara a contagem de duas pessoas sem gravidade

### Requirement: Contagem de caminhões pela regra de composição
O sistema DEVE contar os caminhões de cada ocorrência pelo número de unidades tratoras, entendidas como caminhão e caminhão-trator. O semirreboque e o reboque NÃO recebem valor próprio. Quando houver carreta e nenhuma unidade tratora, a contagem DEVE ser de um caminhão.

#### Scenario: Cavalo mecânico com semirreboque
- **GIVEN** uma ocorrência com um caminhão-trator e um semirreboque
- **WHEN** os veículos são contados
- **THEN** a contagem da classe Caminhões é 1

#### Scenario: Bitrem, uma tratora com duas carretas (caso de borda)
- **GIVEN** uma ocorrência com um caminhão-trator e dois semirreboques
- **WHEN** os veículos são contados
- **THEN** a contagem da classe Caminhões é 1

#### Scenario: Carreta sem unidade tratora registrada (caso de borda)
- **GIVEN** uma ocorrência com um semirreboque, um automóvel e nenhuma unidade tratora
- **WHEN** os veículos são contados
- **THEN** a contagem da classe Caminhões é 1, e a de Automóveis é 1

### Requirement: Custo associado aos veículos
O sistema DEVE mapear cada tipo de veículo da PRF para uma das sete classes do IPEA e somar a contagem de cada classe multiplicada pelo total da Tabela 1B na coluna da ocorrência.

#### Scenario: Motoneta é valorada como motocicleta
- **GIVEN** uma ocorrência com fatalidade, com uma motoneta
- **WHEN** o custo dos veículos é calculado
- **THEN** o subtotal é R$ 4.269,83, o valor da classe Motocicletas

#### Scenario: Tipo de veículo fora do mapeamento (caso de borda)
- **GIVEN** uma ocorrência com um tipo de veículo ausente da tabela de mapeamento
- **WHEN** o cálculo é executado
- **THEN** uma exceção de tipo não mapeado é levantada, e o sistema NÃO atribui a classe Outros por omissão

### Requirement: Custo institucional e patrimonial
O sistema DEVE somar o bloco institucional uma vez por ocorrência, independentemente do número de pessoas e de veículos.

#### Scenario: Ocorrência sem veículo registrado
- **GIVEN** uma ocorrência sem vítimas e sem nenhum veículo registrado
- **WHEN** o cálculo é executado
- **THEN** o custo em dezembro de 2014 é R$ 453,35, apenas o bloco institucional

### Requirement: Atualização monetária com base única
O sistema DEVE aplicar o deflator ao total da ocorrência, ao final do cálculo, e NÃO componente a componente. A base é junho de 2026, com fator 1,884802.

#### Scenario: Reproduzir o exemplo trabalhado da memória de cálculo
- **GIVEN** a ocorrência com dois mortos, um ileso, uma motoneta e um automóvel, classificada com fatalidade
- **WHEN** o cálculo é executado
- **THEN** o total em dezembro de 2014 é R$ 892.660,12
- **AND** o total em junho de 2026 é R$ 1.682.487,58

#### Scenario: Conferir o deflator contra a planilha V07
- **GIVEN** o custo do acidente sem vítimas de R$ 23.498,77, em dezembro de 2014
- **WHEN** o deflator é aplicado
- **THEN** o resultado é R$ 44.290,53, o valor registrado na aba de parâmetros da V07

### Requirement: Saída decomposta por categoria
O sistema DEVE devolver o custo decomposto, em duas leituras: o custo unitário por vítima, nas categorias leve, grave e óbito; e o custo total por ocorrência, nas categorias sem vítimas, com vítima leve, com vítima grave e com óbito, pela vítima mais grave do evento.

#### Scenario: Classificar a ocorrência pela vítima mais grave
- **GIVEN** uma ocorrência com um ferido leve e um ferido grave
- **WHEN** a leitura por ocorrência é montada
- **THEN** a ocorrência entra na categoria com vítima grave
