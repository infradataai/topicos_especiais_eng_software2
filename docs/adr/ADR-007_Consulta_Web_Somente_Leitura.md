# ADR-007 - Consulta web somente leitura

Formato MADR. Numeracao propria da sandbox da disciplina.

- Status: ACEITO
- Data: 2026-09-09
- Decisor: Bruno dos Santos Fernandes da Silva
- Relaciona-se com: ADR-002 (MCP), ADR-003 (monolito modular), ADR-005 (proveniencia)

## Contexto

Usuarios precisam consultar registros consolidados, fontes, lotes e metadados
sem abrir o SQLite manualmente. O acesso web nao pode permitir escrita nem
SQL arbitrario.

## Decisao

A consulta web sera uma fronteira de aplicacao dentro do monolito, separada
dos modulos de ingestao. A API oferecera apenas consultas parametrizadas para
registros, fontes e lotes, com filtros documentados, ordenacao e paginacao.

A aplicacao exibira a proveniencia do registro consultado. A camada web tera
acesso somente leitura; toda escrita continuara restrita ao codigo revisado de
ingestao. SQL recebido do cliente sera rejeitado e nunca executado.

Esta aplicacao nao sera adicionada como servidor MCP. MCP permanece restrito
aos servidores e permissoes do ADR-002.

## Consequencias

A consulta e direta e auditavel, com uma superficie de escrita pequena. A
paginacao evita carregar tabelas inteiras. Autenticacao e autorizacao corporativas
continuam sendo uma dependencia de implantacao e devem ser definidas antes de
expor a aplicacao fora do ambiente local.

## Alternativas consideradas

Expor o SQLite diretamente foi rejeitado por acoplamento e risco de escrita.
Permitir SQL livre foi rejeitado por seguranca e falta de contrato. Criar um
servico independente foi rejeitado enquanto a escala nao justificar a separacao.

## Verificacao

Testes devem cobrir filtros, ordenacao, paginacao, resultado vazio, detalhes de
proveniencia, rejeicao de SQL arbitrario e ausencia de operacoes de escrita.
