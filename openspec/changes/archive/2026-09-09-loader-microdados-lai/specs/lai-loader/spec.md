# Spec (delta) — lai-loader

## ADDED Requirements

### Requirement: Ingestão de arquivos de múltiplas fontes
O sistema DEVE (MUST) aceitar arquivos CSV e XLSX associados a um órgão ou fonte,
usando uma configuração que descreva delimitador, planilha, cabeçalho e
mapeamento das colunas quando a estrutura variar.

#### Scenario: Ingerir CSV e XLSX de órgãos diferentes
- **GIVEN** um CSV do órgão A e um XLSX do órgão B com nomes de coluna diferentes
- **WHEN** cada arquivo é ingerido com sua configuração de fonte
- **THEN** ambos são aceitos, preservados como texto e mapeados para o mesmo esquema canônico

### Requirement: Normalização e deduplicação determinísticas
O sistema DEVE (MUST) normalizar os registros para um esquema canônico e impedir que o
mesmo registro da mesma versão de origem seja consolidado mais de uma vez.

#### Scenario: Reprocessar o mesmo arquivo
- **GIVEN** um arquivo já ingerido com a mesma versão e checksum
- **WHEN** ele é ingerido novamente
- **THEN** nenhum registro canônico duplicado é criado e o lote informa a idempotência

### Requirement: Validação de tipos e inconsistências
O sistema DEVE (MUST) validar colunas obrigatórias, tipos configurados e regras de
consistência, registrando os erros por linha e coluna sem alterar o valor bruto.

#### Scenario: Tipo inválido e coluna ausente
- **GIVEN** um arquivo sem uma coluna obrigatória e com um valor incompatível com o tipo configurado
- **WHEN** a validação é executada
- **THEN** o lote é marcado como inválido, os problemas são reportados e nenhum registro inválido é consolidado

### Requirement: Consolidação relacional e proveniência
O sistema DEVE (MUST) consolidar registros válidos em um banco SQLite único e manter,
para cada lote, órgão, arquivo, checksum, versão, data de ingestão e
configuração utilizada.

#### Scenario: Consultar a origem de um registro
- **GIVEN** um registro válido consolidado a partir de um arquivo versionado
- **WHEN** a origem do registro é consultada
- **THEN** o sistema retorna o lote e os metadados do arquivo de origem

#### Scenario: Arquivo sem dados
- **GIVEN** um CSV ou XLSX com cabeçalho válido e nenhuma linha de dados
- **WHEN** a ingestão é executada
- **THEN** o lote é registrado com zero registros e nenhuma linha canônica é criada
