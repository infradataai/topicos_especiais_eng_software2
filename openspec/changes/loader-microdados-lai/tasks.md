# Tarefas — Carregador de microdados da LAI

- [x] 1. Definir a interface `carregar_csv_lai` e a exceção `ColunasObrigatoriasAusentes`.
- [x] 2. Ler o CSV como texto e validar as colunas obrigatórias.
- [x] 3. Implementar a idempotência via `_row_hash` com `UNIQUE` e `INSERT OR IGNORE`.
- [x] 4. Escrever os testes: carga, idempotência, coluna faltando, arquivo vazio.
- [x] 5. Rodar `pytest` e confirmar os quatro cenários.

Ordem escolhida para destravar a verificação cedo: a interface e a validação vêm antes da idempotência, e os testes acompanham cada regra. As tarefas ficam restritas a `src/lai_loader.py` e `tests/test_lai_loader.py`.
