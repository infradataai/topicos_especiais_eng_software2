**Universidade Federal do Rio Grande do Norte**
**Instituto Metrópole Digital**
**Programa de Pós-Graduação em Tecnologia da Informação**
**Disciplina:** Tópicos Avançados em Engenharia de Software 2 (Desenv. de Software com IA)
**Professor:** Jean Mário Moreira de Lima
**Aluno:** Flávio Eduardo Batista Moreira

# Relatório — Atividade Assíncrona 3

## Harness e Arquitetura na Prática

**Repositório:** https://github.com/infradataai/topicos_especiais_eng_software2 (branch `feature/harness-arquitetura`)

## 1. Autonomia e guardrail

Comparei dois modos de permissão do agente numa tarefa pequena. O plan mode dá mais controle e menos risco, ao custo de mais interações, e compensa em código sensível como o ETL e o banco; o auto-accept é mais rápido para uma função pequena com teste, ao preço de revisar o diff só depois de aplicado. Como guardrail, criei um hook PreToolUse que bloqueia versionar arquivos de dados, risco real porque os microdados da PRF e da LAI têm dado pessoal. O hook barrou de fato o `git add` de um `.db` e de um `.csv` (exit 2) e liberou o código (exit 0).

## 2. TDD e enforcement

Apliquei Red-Green-Refactor na detecção de outliers por IQR, com o teste escrito antes da implementação, o que ficou registrado no histórico (commit do teste que falha, depois o da implementação que passa). Investiguei o TDD Guard, um hook que bloqueia a escrita de implementação sem um teste falhando; no nosso cenário, ele teria barrado a função de outliers antes do Red. A comparação com e sem TDD foi clara: a função feita com teste primeiro nasceu com os casos de borda cobertos, enquanto a função escrita direto deixou passar uma entrada inválida, só notada por um teste posterior.

## 3. Checkpoint humano

Defini como checkpoint obrigatório a fronteira de escrita no banco consolidado, por ser a fonte de todos os resultados a jusante. Na simulação, a execução parou antes da escrita e a decisão foi aprovar com edição, fixando o nome da tabela e as colunas obrigatórias. O papel assumido foi o de Approver, que aprova o marco sem executar cada passo.

## 4. Decisão arquitetural, ADR e diagrama

O resumo da arquitetura, feito a partir do código, mostrou cinco módulos sem acoplamento entre si. A decisão, registrada no ADR-003 em formato MADR, foi manter o monólito modular, porque o acoplamento já é mínimo e um agente raciocina melhor com a lógica co-localizada. Gerei o diagrama de contêiner em duas versões, um fluxograma Mermaid e um C4 Container, e concluí que o fluxograma comunica melhor no dia a dia da equipe e o C4 serve melhor a uma apresentação.

## 5. Etapa 6 e aprendizado

Investiguei as três frentes. Na dívida técnica, o ruff apontou um `zip` sem `strict`, risco de perda silenciosa de dados, que corrigi declarando a intenção. No custo, estimei a tarefa de TDD em oito a doze chamadas ao modelo e propus cache de prompt sobre os arquivos de contexto e model routing. No paralelismo, planejei dois git worktrees para os dois agentes do projeto e mapeei os conflitos de arquivo e de banco. O aprendizado central é que o isolamento resolve o conflito, mas a coordenação é o que evita retrabalho e corrupção de dado.

## 6. Dificuldade enfrentada

A dificuldade foi de coordenação de branches. Comecei a Etapa 1 antes de mesclar o Pull Request da Assíncrona 2, e um arquivo acabou criado em branch errada, como stub. A correção foi mesclar o Pull Request anterior na main, recriar a branch da atividade a partir dela e refazer a edição sobre o código real. A lição prática: construir uma etapa sobre trabalho ainda não integrado gera exatamente o tipo de conflito que a aula de arquitetura descreve.

## Checklist final de entregáveis

- Comparação entre os dois modos de autonomia (Etapa 1): sim, em `docs/harness-etapa1.md`.
- Hook funcional commitado, com evidência do bloqueio (Etapa 1): sim, `.claude/hooks/block_data_commit.py` e evidência no doc.
- Ciclo Red-Green-Refactor e ferramenta de enforcement investigada (Etapa 2): sim, no histórico de commits e em `docs/tdd-etapa2.md`.
- Comparação entre a tarefa com e sem TDD (Etapa 2): sim, em `docs/tdd-etapa2.md`.
- Log/transcript da sessão (Etapa 3): sim, em `docs/sessao-log.md`.
- Resumo da arquitetura, sinal identificado e decisão justificada (Etapa 4): sim, em `docs/arquitetura-etapa4.md`.
- ADR e diagrama commitados, com comparação das duas versões (Etapa 5): sim, `docs/adr/ADR-003_Manter_Monolito_Modular.md` e `docs/diagrama-arquitetura.md`.
- Evidência da opção escolhida na Etapa 6: sim, `docs/etapa6-escala.md` (dívida com ruff, custo e paralelismo com worktrees).
- Repositório no GitHub com histórico de commits real (Etapa 7): sim, branch `feature/harness-arquitetura`, um commit por etapa.
- Relatório final de até uma página (Etapa 8): este documento.
