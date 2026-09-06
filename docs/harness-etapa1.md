# Etapa 1 — Harness mínimo: autonomia e guardrail

## Tarefa pequena usada na comparação

A tarefa foi acrescentar uma função utilitária `contar_linhas(con, tabela)` em `src/lai_validador.py`, com um teste correspondente. É pequena, isolada e verificável por pytest, o que a torna adequada para comparar modos de autonomia sem risco.

## Dois modos de autonomia comparados

A mesma tarefa foi executada duas vezes, em dois modos de permissão do agente.

| Dimensão | Plan mode | Auto-accept edits |
|---|---|---|
| Tempo gasto | [preencher com o seu tempo real] | [preencher com o seu tempo real] |
| Sensação de controle | Alta: o agente só lê e propõe o plano; nada é escrito sem aprovação | Média: as edições entram sozinhas, a revisão vem depois |
| Risco percebido | Baixo: nenhuma edição ou comando roda antes da aprovação | Maior: uma edição errada é aplicada antes de eu ver |
| Quando usar | Mudança que toca ETL, banco ou fronteiras de módulo | Tarefa pequena, isolada e coberta por teste |

Leitura da comparação: o plan mode custa mais interações e tempo, mas mantém o humano como aprovador antes de qualquer escrita, o que compensa em código sensível (ETL, banco). O auto-accept é mais rápido e fluido para uma função pequena com teste, ao preço de revisar o diff só depois de aplicado. A regra prática da aula se confirma: começar restrito e ampliar a autonomia conforme a confiança e a cobertura de testes crescem.

## Guardrail: hook que bloqueia versionar dados

O risco escolhido é próprio do projeto e diferente do exemplo de aula (bloquear merge na main): **impedir que arquivos de dados entrem no repositório**. Os microdados da PRF e da LAI contêm informação pessoal (boletins de acidente), e os bancos são pesados; versioná-los por engano vaza dado sensível e incha o histórico.

O hook `.claude/hooks/block_data_commit.py` roda como `PreToolUse` sobre a ferramenta Bash (configurado em `.claude/settings.json`). Ele inspeciona o comando; se for um `git add` ou `git commit` que referencie uma extensão de dados (`.db`, `.csv`, `.xlsx`, `.xls`, `.parquet`, `.sqlite`), encerra com `exit 2`, o que bloqueia a ação no Claude Code. Ele complementa o `.gitignore`: o `.gitignore` evita o `git add .`, e o hook barra a inclusão explícita de um arquivo de dados.

## Evidência do bloqueio funcionando

Execução real do hook com três entradas simuladas:

```text
TESTE 1: git add rebuild/tese_brV02.db
  -> BLOQUEADO pelo hook block_data_commit: ... nao devem entrar no repositorio.
  -> exit=2

TESTE 2: git commit -m x concedidos-01-2022.csv
  -> BLOQUEADO pelo hook block_data_commit: ...
  -> exit=2

TESTE 3: git add src/lai_loader.py
  -> (sem saida)
  -> exit=0
```

Os dois comandos que tentam versionar dados são bloqueados com `exit 2`; o comando que versiona código é liberado com `exit 0`. O guardrail atua de fato, não apenas no papel.

## Ligação com o projeto final

Este guardrail é diretamente reaproveitável no projeto final (piloto RN de custo social), que também ingere dados de múltiplos órgãos com informação pessoal. O hook impede o vazamento acidental desses dados pelo controle de versão, uma exigência real quando o repositório for compartilhado com o colega de dupla.
