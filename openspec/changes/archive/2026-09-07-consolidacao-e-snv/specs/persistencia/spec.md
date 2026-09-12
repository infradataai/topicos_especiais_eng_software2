# Spec (delta) — persistencia

## ADDED Requirements

### Requirement: Esquema relacional único
O sistema DEVE consolidar as tabelas de grão único num banco SQLite, com esquema declarado por SQLAlchemy, preservando as chaves de cada grão: ocorrências por identificador, veículos e pessoas pelas suas chaves compostas, segmentos do SNV por código e safra, e o custo por ocorrência.

#### Scenario: Criar o esquema num banco novo
- **GIVEN** um caminho de banco que ainda não existe
- **WHEN** a criação do esquema é executada
- **THEN** o banco é criado com as tabelas declaradas, e a consulta a qualquer uma delas devolve zero linhas

### Requirement: Carga idempotente
O sistema DEVE carregar uma tabela sem duplicar linhas quando a mesma origem for carregada de novo. A idempotência DEVE se apoiar na chave do grão, e NÃO na ordem ou na quantidade de linhas.

#### Scenario: Recarregar a mesma origem
- **GIVEN** um conjunto de ocorrências já carregado
- **WHEN** a mesma carga é executada uma segunda vez
- **THEN** a contagem de linhas permanece a mesma

#### Scenario: Carga parcialmente nova
- **GIVEN** um conjunto já carregado e um novo conjunto que repete metade das chaves
- **WHEN** a segunda carga é executada
- **THEN** apenas as chaves inéditas são inseridas

### Requirement: Rastreamento de origem e versão
Cada linha carregada DEVE registrar a sua proveniência: o órgão de origem, o nome do arquivo, a safra ou o ano de referência e o instante da carga. A proveniência DEVE ser consultável por tabela.

#### Scenario: Consultar a proveniência de uma carga
- **GIVEN** uma carga de ocorrências da PRF do ano de 2024
- **WHEN** a proveniência da tabela é consultada
- **THEN** o registro traz o órgão `PRF`, o arquivo de origem, o ano `2024` e o instante da carga

#### Scenario: Duas origens na mesma tabela
- **GIVEN** cargas de dois anos diferentes na mesma tabela
- **WHEN** a proveniência é consultada
- **THEN** os dois registros aparecem, cada um com o seu arquivo e ano

### Requirement: Consulta por unidade da federação
O sistema DEVE permitir recuperar as ocorrências, os segmentos e o custo agregado filtrando pela unidade da federação, que é o parâmetro de escala do projeto.

#### Scenario: Recuperar o custo por segmento de uma UF
- **GIVEN** um banco com ocorrências de duas unidades da federação
- **WHEN** o custo por segmento é consultado para `RN`
- **THEN** apenas os segmentos daquele estado são devolvidos

### Requirement: Nenhum dado pessoal no banco versionado
O banco consolidado DEVE residir na pasta de dados, fora do controle de versão, e o sistema NÃO DEVE gravar nele campos que identifiquem pessoas além dos identificadores técnicos já publicados pela PRF.

#### Scenario: Caminho do banco na pasta de dados
- **GIVEN** a configuração padrão do projeto
- **WHEN** o caminho do banco é resolvido
- **THEN** ele aponta para a pasta de dados, coberta pelo `.gitignore`
