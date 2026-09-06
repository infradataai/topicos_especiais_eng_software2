# Tarefas — Validador de qualidade

- [x] 1. Ler as colunas da tabela e contar as linhas.
- [x] 2. Calcular colunas ausentes e vazios por coluna.
- [x] 3. Calcular duplicatas por comparação de linhas distintas.
- [x] 4. Calcular datas fora da faixa a partir do ano na coluna de data.
- [x] 5. Compor o indicador `ok`.
- [x] 6. Escrever os testes dos três cenários e rodar `pytest`.

Revisão do plano: a ordem coloca as métricas simples antes do indicador agregado `ok`, que depende de todas. Cada tarefa fica restrita a `src/lai_validador.py` e `tests/test_lai_validador.py`. Nenhuma tarefa escreve em banco.
