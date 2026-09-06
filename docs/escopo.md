# Escopo — Atividade Assíncrona 2 (SDD)

Disciplina Tópicos Avançados em Engenharia de Software 2, PPgTI/UFRN. Estudo de caso: o fio da LAI do pipeline M-LRSDI, a obtenção e a estruturação dos dados obtidos por pedidos de acesso à informação.

## Funcionalidades escolhidas

**Funcionalidade 1 — Carregador de microdados da LAI para SQLite.** Lê um arquivo CSV de microdados (por exemplo os benefícios do INSS já baixados) e o carrega em uma tabela da camada bronze, validando as colunas obrigatórias. Cenários de uso: carregar um arquivo mensal novo; recarregar um arquivo já processado sem duplicar linhas. Ferramenta de spec: OpenSpec.

**Funcionalidade 2 — Validador de qualidade dos dados carregados.** Inspeciona uma tabela já carregada e emite um relatório de qualidade: contagem de linhas, colunas ausentes, vazios por coluna, duplicatas e datas fora de faixa. Cenários de uso: validar logo após uma carga; comparar duas cargas ao longo do tempo. Ferramenta de spec: GitHub Spec-Kit.

**Funcionalidade 3 — Parser de tabela de uma resposta da LAI em PDF.** Extrai a tabela de uma resposta em PDF e a converte em registros para carga no banco. Cenários de uso: extrair a tabela de um PDF com cabeçalho e linhas; tratar um PDF sem tabela útil. Ferramenta de spec: OpenSpec.

## Por que são bons casos para SDD

As três funcionalidades têm regras de negócio que um agente não adivinha sozinho, o que as afasta do vibe coding. O carregador precisa da leitura como texto imutável e da idempotência, decisões ligadas aos ADRs de determinismo e camada bronze da tese. O validador depende de critérios objetivos de qualidade, que só valem se forem explicitados como limites testáveis. O parser de PDF concentra casos de borda difíceis: PDF sem tabela, células faltantes, linhas em branco. Cada funcionalidade toca mais de um arquivo (código, teste e, no caso da carga, esquema do banco) e tem pelo menos dois cenários de uso distintos, o que exige uma especificação de verdade, com critérios de aceite e casos de borda declarados antes do código.
