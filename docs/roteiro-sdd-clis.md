# Roteiro das CLIs de SDD (OpenSpec e Spec-Kit)

Os artefatos deste repositório seguem o formato de cada ferramenta. Este roteiro
mostra como rodar as CLIs para reproduzir ou regenerar esses artefatos e ter o
histórico real do processo.

## OpenSpec (funcionalidades 1 e 3)

```bash
# Instalar (Node)
npm install -g openspec

# Inicializar no projeto (gera instruções para o agente)
openspec init

# Propor uma mudança a partir da intenção
openspec change new "carregador de microdados da LAI para SQLite"
# -> gera openspec/changes/<slug>/proposal.md, specs/, design.md, tasks.md

# Revisar os artefatos; aprovado o plano, aplicar tarefa a tarefa
openspec apply carregador-de-microdados-da-lai-para-sqlite

# Depois de validado, arquivar (a spec vira histórico)
openspec archive carregador-de-microdados-da-lai-para-sqlite
```

Repita `openspec change new` para a funcionalidade 3 (parser de PDF).

## GitHub Spec-Kit (funcionalidade 2)

```bash
# Instalar o CLI
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# Inicializar, escolhendo o agente (Claude Code)
specify init .

# Dentro do agente, em sequência:
# 1. Constituição do projeto (uma vez)
/speckit.constitution Priorizar determinismo, testes e nao escrever no banco sem revisao

# 2. Especificar a funcionalidade
/speckit.specify Validador de qualidade dos dados carregados da LAI

# 3. Plano técnico
/speckit.plan Python com sqlite3, sem dependencia nova, apenas leitura

# 4. Tarefas e implementação
/speckit.tasks
/speckit.implement
```

O Spec-Kit grava a constituição em `.specify/memory/constitution.md` e a
funcionalidade em `specs/<feature>/spec.md`, `plan.md` e `tasks.md`.
