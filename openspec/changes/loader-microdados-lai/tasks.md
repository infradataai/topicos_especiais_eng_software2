# Tarefas — Carregador de microdados da LAI

- [x] 1. Definir a interface `carregar_csv_lai` e a exceção `ColunasObrigatoriasAusentes`.
- [x] 2. Ler o CSV como texto e validar as colunas obrigatórias.
- [x] 3. Implementar a idempotência via `_row_hash` com `UNIQUE` e `INSERT OR IGNORE`.
- [x] 4. Escrever os testes: carga, idempotência, coluna faltando, arquivo vazio.
- [x] 5. Rodar `pytest` e confirmar os quatro cenários.
- [ ] 6. Substituir a interface específica por uma configuração de fonte para CSV e XLSX.
- [ ] 7. Criar tabelas de fontes, lotes, bronze e registros canônicos no SQLite.
- [ ] 8. Implementar normalização, validação de tipos e relatório de inconsistências.
- [ ] 9. Implementar deduplicação por checksum, versão e impressão digital canônica.
- [ ] 10. Testar dois órgãos, dois formatos, reprocessamento e consulta de proveniência.

Ordem escolhida para destravar a verificação cedo: a interface e a validação vêm antes da idempotência, e os testes acompanham cada regra. As tarefas ficam restritas ao carregador, ao esquema SQLite e aos testes da ingestão. Nenhuma conversão deve sobrescrever a cópia bronze.
