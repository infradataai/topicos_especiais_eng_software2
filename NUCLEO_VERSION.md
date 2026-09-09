# Origem do núcleo

Este repositório é a fonte única do núcleo `custo_social_core`, conforme o
`docs/adr/ADR-013_Consolidacao_do_Trabalho_no_Repositorio_da_Disciplina.md`.

A fonte mudou duas vezes. Até 07/09/2026 o núcleo vivia aqui, e o repositório privado
consumia uma cópia controlada, como o ADR-004 decidiu. Em 07/09 a relação se inverteu,
pelo ADR-010, quando os dados e a execução passaram a viver no privado. Em 09/09 ela
voltou, pelo ADR-013, quando os dois autores consolidaram o trabalho aqui para a entrega
da disciplina.

- Repositório privado da escala nacional: https://github.com/infradataai/custo-social-sinistro-BR
- O que fica lá: os arquivos de origem, com 35 GB entre PRF, SNV, RENAEST e DATASUS, e a
  ingestão do RENAEST prevista para depois da apresentação.
- O que fica aqui: o núcleo, a camada de aplicação, os scripts, os testes, os ADRs, o
  pacote OpenSpec, os documentos de análise e o `dados/consolidado.db`.

Ao rodar uma carga nova no repositório privado, registre aqui o commit correspondente,
para manter as duas pontas rastreáveis.
