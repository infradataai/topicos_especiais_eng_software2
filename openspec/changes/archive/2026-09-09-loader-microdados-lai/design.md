A leitura usa pandas com `dtype=str` para CSV e XLSX, preservando a camada
bronze. Uma configuração por órgão informa delimitador, planilha, linha de
cabeçalho, mapeamento de colunas e regras de tipo. A normalização produz um
esquema canônico separado da cópia bruta.

Cada execução cria um lote com órgão, arquivo, checksum, versão, horário e
configuração usada. As tabelas de origem, lotes e registros normalizados ficam
no mesmo SQLite. A deduplicação usa uma impressão digital determinística da
origem, versão e valores canônicos; reprocessar o mesmo lote é idempotente.
Valores que não obedecem ao tipo ou às regras de consistência são registrados
no relatório do lote e não são convertidos silenciosamente.
Apagar e recriar tabelas foi rejeitado porque perde histórico. Deduplicar só em
memória foi rejeitado porque não protege recargas separadas. Uma chave de
negócio única foi rejeitada porque fontes externas podem não fornecê-la.

## Interface

`ingerir_arquivo(caminho, fonte, con, configuracao) -> RelatorioCarga`, que
aceita `.csv` ou `.xlsx`, devolve métricas do lote e grava bronze, catálogo de
fontes, erros de qualidade e registros canônicos no SQLite.
