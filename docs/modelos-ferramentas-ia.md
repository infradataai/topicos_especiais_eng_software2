# Modelos, estratégias e ferramentas de IA

Projeto Final da disciplina Tópicos Avançados em Engenharia de Software 2 (PPgTI/UFRN, 2026.2). Prof. Dr. Jean Mário Moreira de Lima.

Dupla: Flávio Eduardo Batista Moreira e Bruno dos Santos Fernandes da Silva.

Este documento reúne, em lista objetiva, os modelos de IA, as ferramentas e as estratégias de prompt usadas ao longo do desenvolvimento do piloto de custo social dos sinistros (RN) e do seu ensaio de escala nacional. Cada item aponta o artefato do repositório que o comprova.

## Modelos de IA

| Modelo | Papel no projeto | Evidência |
|---|---|---|
| GPT 5.3-Luna (OpenAI) | Geração e revisão de código no editor; selecionado automaticamente pelo GitHub Copilot ou pelo Claude Code. | `.github/`, `.claude/` |
| Opus 4.8 (Anthropic) | Idem; nas tarefas de maior complexidade. | `.github/`, `.claude/` |
| Claude Sonnet (Anthropic) | Idem; uso corrente ao longo do projeto. | `.github/`, `.claude/` |

A seleção do modelo foi automática, feita pelo Claude Code ou pelo GitHub Copilot, e recaiu quase sempre em um destes três. O comparativo da Etapa 4 (`docs/prompts-comparacao.md`) registrou um achado metodológico: num problema pequeno e bem delimitado, um contexto de prompt bem escrito recupera boa parte da diferença de capacidade entre modelos.

## Ferramentas

| Categoria | Ferramenta | Uso | Evidência |
|---|---|---|---|
| IDE | VS Code + GitHub Copilot + Claude Code | Edição e sugestão de código no editor, com seleção automática de modelo. | `.github/`, `.claude/` |
| Agente de linha de comando | Claude Code | Execução em ramo isolado, edição de arquivos, testes e checkpoints. | `.claude/` |
| Harness — permissões | `.claude/settings.json` | Nega `git push --force`, `git reset --hard` e a leitura de `.env`; exige confirmação para `git push` e coletas pesadas; libera git de leitura, commit e `pytest`. | `.claude/settings.json` |
| Harness — regra por escopo | `.claude/rules/notebooks.md` | Restringe os notebooks de ETL e EDA: leem a camada ouro e nunca escrevem no banco; a bronze é lida como texto imutável. | `.claude/rules/notebooks.md` |
| Contexto de projeto | `CLAUDE.md` e `AGENTS.md` | Contexto persistente lido pelos agentes a cada sessão. | raiz do repositório |
| Servidores MCP | `sqlite-ouro` e `fs-lai` | Acesso ao banco ouro e ao diretório da LAI, ambos em leitura. | `.mcp.json` |
| Ferramenta de spec (SDD) | OpenSpec | Mudanças em pasta própria (`proposal`, `specs` em delta, `design`, `tasks`), no trabalho incremental sobre código existente. | `openspec/changes/` |
| Testes | Pytest (TDD/BDD) | 106 testes na árvore consolidada (30 da camada de aplicação e 76 do núcleo). | `tests/`, ADR-013 |

## Estratégias de prompt

O comparativo da Etapa 4 (`docs/prompts-comparacao.md`) fixou o padrão de prompt adotado no projeto, em quatro partes:

1. **Contexto** — a linguagem, o módulo de destino e o estado atual do dado (por exemplo, a coluna lida como texto).
2. **Padrão a seguir** — a convenção do projeto registrada em ADR (por exemplo, o `dayfirst=True` do parsing de data).
3. **Restrições** — o que a solução não pode fazer (sem dependências novas, sem efeito colateral, sem exceção em valor inválido).
4. **Validação** — o teste que a resposta precisa passar.

Duas estratégias complementares sustentaram o processo. Primeira: a especificação antes do código, com os critérios de aceite em Given/When/Then e ao menos um caso de borda, de modo que a decisão estrutural ficasse na spec e não na geração do agente. Segunda: a revisão de diff antes de cada aceite, com o merge condicionado ao checkpoint humano.

## Observabilidade e controle

O controle sobre os agentes se apoiou em três mecanismos verificáveis: o transcript de cada sessão, a revisão do diff antes do aceite e as permissões declaradas em `.claude/settings.json`, que bloqueiam de fato as operações destrutivas. Nada entra no `main` sem esse rastro.

---
