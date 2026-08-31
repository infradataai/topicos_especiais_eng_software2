# Plano técnico — Validador de qualidade

## Stack e arquitetura

Python com a biblioteca padrão `sqlite3`, sem dependência nova. Uma única função `validar_tabela` que abre consultas de leitura sobre a tabela e monta um dicionário de relatório. Nenhuma escrita, coerente com a constituição.

## Decisões

As métricas usam SQL agregado (`COUNT`, `DISTINCT`) em vez de carregar a tabela em memória, o que escala para tabelas grandes. A coluna técnica `_row_hash` é ignorada nas métricas de negócio. O indicador `ok` combina linhas maiores que zero, nenhuma coluna faltando, zero duplicatas e zero datas fora da faixa.

## Interface

`validar_tabela(con, tabela, colunas_esperadas=None, coluna_data=None, ano_min=None, ano_max=None) -> dict`.
