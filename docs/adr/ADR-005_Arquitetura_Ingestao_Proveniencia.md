# ADR-005 - Arquitetura de ingestao, consolidacao e proveniencia

Formato MADR. Numeracao propria da sandbox da disciplina.

- Status: ACEITO
- Data: 2026-09-09
- Decisor: Bruno dos Santos Fernandes da Silva
- Relaciona-se com: ADR-002 (fronteiras de acesso), ADR-003 (monolito modular)

## Contexto

Os dados chegam de varios orgaos em CSV e XLSX, com delimitadores, planilhas,
cabecalhos, nomes de coluna e representacoes de tipos diferentes. O sistema
precisa preservar a entrada, normalizar registros, detectar problemas,
consolidar dados e permitir rastrear a origem de cada registro.

## Decisao

Adotar quatro responsabilidades no mesmo monolito:

1. Bronze: copia fiel dos valores recebidos, lidos como texto e nunca sobrescrita
   por normalizacao.
2. Catalogo de fontes e lotes: orgao, arquivo, checksum, versao, configuracao,
   data de ingestao e resultado da validacao.
3. Camada canonica: registros validos normalizados em tabelas SQLite relacionais.
4. Qualidade: inconsistencias de tipo, obrigatoriedade e regras de dominio
   registradas por lote, linha e coluna.

A ingestao usa configuracao explicita por fonte para delimitador, planilha,
cabecalho, mapeamento e tipos. A deduplicacao usa checksum, versao e impressao
digital deterministica dos valores canonicos. Registros invalidos nao sao
consolidados nem corrigidos silenciosamente.

## Consequencias

A origem e a versao ficam consultaveis sem reprocessar o arquivo. A bronze pode
ser auditada e a camada canonica pode ser consumida pela analise, web e relatorios.
O custo e manter configuracoes por fonte e tabelas de metadados. Mudancas no
esquema canonico exigem migracao e atualizacao das specs.

## Alternativas consideradas

Carregar diretamente na tabela final foi rejeitado porque mistura preservacao,
normalizacao e auditoria. Inferir tipos sem configuracao foi rejeitado porque
pode converter valores de forma silenciosa. Um banco separado por orgao foi
rejeitado porque dificulta consultas e consolidacao.

## Verificacao

Cada carga deve possuir teste de CSV, XLSX, dois orgaos, reprocessamento,
registro de inconsistencias e consulta de proveniencia. Nenhum consumidor pode
escrever na bronze.
