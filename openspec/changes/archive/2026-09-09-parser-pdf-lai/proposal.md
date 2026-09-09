# Proposta — Parser de tabela de uma resposta da LAI em PDF

## Por quê

Parte das respostas da LAI chega em PDF, com a informação em tabela. Extrair essas tabelas à mão é lento e sujeito a erro. Uma extração padronizada permite levar o conteúdo do PDF para o banco com a mesma disciplina dos microdados em CSV.

## O que muda

Adiciona uma função que extrai a primeira tabela de uma página do PDF e a converte em registros, separando a leitura do PDF da normalização das linhas, para que a lógica de normalização seja testável sem um arquivo real.

## Fora de escopo

Reconhecimento de texto em PDF escaneado (OCR). Múltiplas tabelas por página. Carga no banco, que reaproveita o carregador da funcionalidade 1.
