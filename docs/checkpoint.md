# Checkpoint humano e revisão de diff

## Revisão de diff (Etapa 3)

Durante a implementação do carregador, a revisão do diff pegou um ponto que teria passado sem atenção. A primeira versão inseria as linhas com `INSERT`, sem a cláusula `OR IGNORE` nem a restrição `UNIQUE` sobre `_row_hash`. O código passava no teste de carga simples, mas a idempotência só apareceu como requisito ao reler a especificação. A revisão do diff exigiu o `INSERT OR IGNORE` e a restrição `UNIQUE`, sem os quais uma recarga do mesmo arquivo duplicaria as linhas na camada bronze. O teste de idempotência foi acrescentado para travar essa regra.

## Checkpoint humano obrigatório (Etapa 4)

O checkpoint definido para este projeto é a fronteira de escrita no banco. Nenhuma carga que grave em uma tabela SQLite ocorre sem revisão humana do diff e confirmação explícita. A escolha se justifica porque a camada bronze é imutável e a integridade dela sustenta todos os resultados a jusante da tese.

## Simulação do checkpoint

O ponto de parada foi simulado antes da primeira carga real. O agente propôs executar o carregador sobre um arquivo de microdados do INSS, apontando para uma tabela nova. A execução foi interrompida no checkpoint. A decisão registrada foi aprovar com edição: a tabela de destino recebeu um nome com prefixo de camada (`bronze_lai_inss`) e o conjunto de colunas obrigatórias foi fixado antes de liberar a carga. O papel humano assumido foi o de revisor responsável pela integridade da camada bronze, que aprova o esquema e o destino antes de qualquer escrita.
