# Etapa 6 — Escala: dívida técnica, custo e paralelismo

A atividade pede uma investigação; as três foram feitas, porque juntas cobrem todo o tema de escala da aula.

## Opção A — Dívida técnica (análise estática com ruff)

Rodei o `ruff` sobre o `src/`, primeiro com as regras padrão e depois com um conjunto mais rígido (complexidade, bugbear, simplificação, uso de pathlib):

```text
ruff check src/ --select E,F,W,C90,B,SIM,PTH --statistics
  3  E501  line-too-long
  1  B905  zip-without-explicit-strict
```

O sinal real mais relevante é o **B905 (`zip-without-explicit-strict`)**, em `src/lai_pdf_parser.py`, no `dict(zip(cabecalho, valores))`. Num pipeline de dados, `zip` sem o parâmetro `strict` é dívida técnica de verdade: se o cabeçalho e a linha tiverem tamanhos diferentes, o `zip` trunca em silêncio, perdendo colunas sem erro. Hoje a função preenche as células faltantes antes do `zip`, então o risco está contido, mas a intenção não está declarada.

Mitigação proposta: tornar a intenção explícita com `strict=False` (aceito truncar de propósito, já que padronizo o tamanho antes) ou, melhor, `strict=True` com um teste que garanta o pré-preenchimento, transformando um comportamento implícito em contrato verificável. As três linhas longas (E501) são formatação e se resolvem com `ruff format`. O `EXE002` observado nas regras padrão é artefato do sistema de arquivos (bit de executável), não do código.

## Opção B — Custo e performance

Estimativa para uma tarefa recente, a implementação da detecção de outliers por TDD (Etapa 2). Um agente não faz uma chamada por tarefa: ele lê o contexto, planeja, edita, roda o pytest, observa e itera. Para essa tarefa pequena, uma estimativa justificada é de oito a doze chamadas ao modelo, dominadas pela leitura de contexto (a aula cita proporção de 166 tokens lidos para cada 1 gerado). Com os arquivos de contexto do projeto (`AGENTS.md`, `CLAUDE.md`) relidos a cada chamada, o custo por tarefa fica na faixa de alguns dólares, coerente com a estimativa de 5 a 8 dólares da aula para uma tarefa de engenharia sem otimização.

Otimização proposta para o nosso contexto: **cache de prompt**. Os arquivos `AGENTS.md` e `CLAUDE.md` e as convenções do projeto são relidos em toda sessão e em quase toda chamada; colocá-los no trecho cacheável reaproveita esses tokens entre chamadas, com economia relatada de até 90% nos tokens que acertam o cache. Como complemento, **model routing**: as tarefas pequenas e bem escopadas (como a `contar_linhas` ou a implementação Green sob um teste que já existe) podem ir para um modelo mais barato, reservando o modelo de raciocínio forte para a especificação e o plano, onde o erro é mais caro. A métrica que guia a decisão é o custo por resultado correto, não por token.

## Opção C — Agentes em paralelo (git worktrees)

O projeto final é em dupla, então rodar dois agentes em paralelo é um cenário real. Os dois agentes do nosso escopo (qualidade de dados e acompanhamento da LAI) são tarefas independentes, boas candidatas a worktrees. Os comandos para criar os dois ambientes isolados:

```bash
git worktree add ../TEES-agente-qualidade feature/agente-qualidade
git worktree add ../TEES-agente-lai       feature/agente-lai
# cada agente roda em uma dessas pastas, na sua branch, compartilhando o mesmo .git
```

Conflitos previstos para este projeto, e como tratá-los. O arquivo compartilhado mais quente é o `src/analise.py`, que os dois agentes poderiam tocar; a mitigação é decompor por domínio, um agente por módulo, e fazer merges sequenciais verificados. O banco SQLite é o segundo ponto de conflito: dois agentes escrevendo no mesmo arquivo `.db` corrompem o dado; a mitigação é dar a cada worktree um caminho próprio de banco pela variável de ambiente `TESE_DB`, que o `.mcp.json` já usa. Portas não são um problema no estágio atual, porque ainda não há servidor web; quando o mapa interativo do piloto RN entrar, cada worktree precisará de uma porta distinta. As dependências são compartilhadas pelo mesmo ambiente Python, o que é seguro para leitura, mas recomenda um ambiente virtual por worktree se as versões divergirem.

O aprendizado central bate com a aula: o isolamento (worktree) resolve o conflito de arquivos, mas a coordenação (decomposição por domínio, lista de tarefas compartilhada, merge sequencial) é o que evita retrabalho e corrupção de dado quando dois agentes, ou duas pessoas, trabalham ao mesmo tempo.
