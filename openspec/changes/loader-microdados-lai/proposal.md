# Proposta — Carregador de microdados da LAI para SQLite

## Por quê

Os microdados obtidos por pedidos de acesso à informação (por exemplo os benefícios do INSS) chegam em arquivos CSV e precisam entrar no banco da camada bronze de forma confiável. Sem uma carga padronizada, cada arquivo é importado à mão, com risco de duplicar linhas ao reprocessar e de aceitar arquivos com colunas faltando.

## O que muda

Adiciona uma função de carga que lê o CSV como texto, valida as colunas obrigatórias e insere na tabela de destino de modo idempotente, sem duplicar quando o mesmo arquivo é recarregado.

## Fora de escopo

Transformação, limpeza ou conversão de tipos, que pertencem às camadas a jusante. Leitura de XLSX, tratada como extensão futura. Escrita em qualquer camada além da bronze.
