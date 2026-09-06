# Tarefas — Parser de tabela da LAI em PDF

- [x] 1. Definir `normalizar_linhas` (pura) e a exceção `TabelaVazia`.
- [x] 2. Tratar os casos de borda: linha vazia, célula faltante, tabela sem dados.
- [x] 3. Escrever `extrair_tabela_pdf` como invólucro de pdfplumber.
- [x] 4. Escrever os testes da função pura (quatro cenários).
- [x] 5. Rodar `pytest` e confirmar.

A verificação é destravada cedo ao isolar a lógica pura, testada sem depender do PDF. As tarefas ficam restritas a `src/lai_pdf_parser.py` e `tests/test_lai_pdf_parser.py`.
