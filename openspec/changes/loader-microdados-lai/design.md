# Design — Carregador de microdados da LAI

## Decisões

A leitura usa pandas com `dtype=str`, coerente com a camada bronze imutável, que não converte nem limpa na entrada. A idempotência se apoia em uma coluna técnica `_row_hash`, o SHA-1 da concatenação dos valores da linha, com restrição `UNIQUE` e `INSERT OR IGNORE`. Assim, recarregar o mesmo arquivo não gera duplicatas, e a carga é determinística.

## Alternativas consideradas

Apagar e recriar a tabela a cada carga foi rejeitado porque perde o histórico de cargas incrementais. Deduplicar só em memória foi rejeitado porque não protege contra recarga em execuções separadas. Uma chave primária de negócio foi rejeitada porque os microdados da LAI não têm identificador único garantido.

## Interface

`carregar_csv_lai(caminho_csv, con, tabela, colunas_obrigatorias, sep=",") -> int`, que devolve o número de linhas novas inseridas.
