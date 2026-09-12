# Documento de entrega — Projeto Final

Disciplina Tópicos Avançados em Engenharia de Software 2 (Desenvolvimento de Software com IA). PPgTI · Instituto Metrópole Digital · UFRN, 2026.2. Prof. Dr. Jean Mário Moreira de Lima.

Apresentação: 12/09/2026.

## Dupla

| Nome | Matrícula |
|---|---|
| Flávio Eduardo Batista Moreira | 20251018382 |
| Bruno dos Santos Fernandes da Silva | 20251031992 |

## Projeto

Sistema de medição do custo social dos sinistros nas rodovias federais: um pipeline que ingere dados heterogêneos (PRF, SNV/DNIT, IPEA), calcula o custo por ocorrência em quatro categorias de gravidade, ancora o resultado na geometria oficial do SNV e o entrega num mapa consultável. Piloto no Rio Grande do Norte, com ensaio de escala nacional.

## Links

| Item | Link |
|---|---|
| Repositório do projeto | https://github.com/infradataai/topicos_especiais_eng_software2 |
| Post no LinkedIn (método STAR) | https://www.linkedin.com/feed/update/urn:li:share:7504327913333465088/ |

Observação sobre o repositório: o trabalho final consolidado está na branch `feature/projeto-final-rn`. Antes da apresentação, essa branch deve ser integrada ao `main`, para que a raiz do repositório mostre o pipeline completo. O repositório é público; não é necessário conceder acesso.

## Entregáveis (seção VI)

1. **Código-fonte** no repositório acima, com histórico de commits real.
2. **Apresentação** da defesa (arquivo HTML autossuficiente), cobrindo os sete pontos da seção V.
3. **Documento de modelos, estratégias e ferramentas de IA**: `docs/modelos-ferramentas-ia.md`.
4. **Post no LinkedIn** pelo método STAR: rascunho em `docs/post-linkedin-star.md`; o link publicado entra na tabela acima.

## Correspondência com a seção V (apresentação)

| # | Ponto exigido | Onde é coberto |
|---|---|---|
| 1 | Contexto e motivação | Slide "O problema" |
| 2 | Processo de especificação (SDD) | Slides de SDD e do exemplo Given/When/Then |
| 3 | Harness (autonomia, guardrails, controle) | Slide "Harness" |
| 4 | Decisões de arquitetura (ADR e diagrama) | Slides de diagrama e de ADRs |
| 5 | Modelos, estratégias e ferramentas de IA | Slide de ferramentas e `docs/modelos-ferramentas-ia.md` |
| 6 | Demonstração funcional ao vivo | Slide de demo, mapa em `http://127.0.0.1:8000/mapa` |
| 7 | Aprendizados, dificuldades e o que faria diferente | Slide de retrospectiva |

---

Nota de método: este documento segue a norma culta e a voz impessoal. A revisão final pela rotina de escrita científica humanizada (auditor e diff de integridade) fica pendente do retorno do ambiente de execução.
