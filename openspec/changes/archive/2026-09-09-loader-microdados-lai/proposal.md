# Proposta — Ingestão e consolidação de dados multi-origem

## Por quê

Dados de órgãos diferentes chegam em CSV e XLSX, com delimitadores, planilhas,
cabeçalhos, nomes de coluna e tipos representados de formas diferentes. Sem um
contrato único de ingestão, a consolidação é manual, perde a origem do dado e
fica sujeita a duplicatas e inconsistências silenciosas.

## O que muda

Adiciona uma ingestão orientada por configuração de fonte que lê CSV/XLSX como
texto, registra órgão e versão do arquivo, normaliza para um esquema canônico,
valida tipos e inconsistências, deduplica de forma determinística e consolida
os registros e metadados em um banco SQLite relacional.

## Fora de escopo

OCR de documentos escaneados, inferência automática de significado de colunas
sem configuração e correção silenciosa de valores inválidos. A camada bronze
preserva os valores recebidos; normalização e validação ocorrem em tabelas
derivadas. A ingestão não gera análises estatísticas nem relatórios de usuário.
