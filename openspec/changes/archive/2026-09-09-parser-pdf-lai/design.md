# Design — Parser de tabela da LAI em PDF

## Decisões

A leitura do PDF fica separada da normalização. `normalizar_linhas` é uma função pura que recebe listas de listas e devolve registros, testável sem PDF. `extrair_tabela_pdf` é um invólucro fino que usa pdfplumber e delega à função pura. O import de pdfplumber acontece dentro do invólucro, para que os testes da lógica pura não exijam a dependência.

## Alternativas consideradas

Testar direto sobre um PDF real foi rejeitado por acoplar o teste a um arquivo grande e a uma dependência pesada. Gerar um PDF de teste em tempo de execução foi rejeitado por complexidade desproporcional ao ganho.

## Interface

`normalizar_linhas(linhas) -> list[dict]` e `extrair_tabela_pdf(caminho_pdf, pagina=0) -> list[dict]`, ambas com a exceção `TabelaVazia`.
