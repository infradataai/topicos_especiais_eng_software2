# Spec — Validador de qualidade dos dados carregados da LAI

## User story

Como responsável pela integração dos dados da LAI, quero validar uma tabela recém-carregada, para confiar nos dados antes de usá-los a jusante.

## Requisitos

- O validador DEVE contar as linhas da tabela.
- O validador DEVE listar as colunas ausentes em relação a um conjunto esperado, quando informado.
- O validador DEVE contar os vazios por coluna.
- O validador DEVE contar as linhas duplicadas.
- O validador DEVE contar as datas fora de uma faixa de anos, quando a coluna de data e a faixa forem informadas.
- O validador DEVE devolver um indicador `ok` que resume se a tabela passou.
- O validador NÃO DEVE alterar os dados.

## Critérios de aceite (Given/When/Then)

### Cenário: Tabela íntegra
- **DADO** uma tabela com duas linhas distintas e todas as colunas esperadas
- **QUANDO** o validador roda
- **ENTÃO** o relatório traz duas linhas, nenhuma coluna faltando, zero duplicatas e `ok` verdadeiro

### Cenário: Vazios e duplicatas
- **DADO** uma tabela com duas linhas idênticas e uma coluna vazia
- **QUANDO** o validador roda
- **ENTÃO** o relatório aponta os vazios daquela coluna, uma duplicata e `ok` falso

### Cenário: Coluna faltando e data fora da faixa (caso de borda)
- **DADO** uma tabela sem uma coluna esperada e com uma data do ano 2030
- **QUANDO** o validador roda com faixa de 2019 a 2025
- **ENTÃO** o relatório lista a coluna ausente, conta uma data fora da faixa e `ok` falso
