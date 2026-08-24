# Tese_BR_TEES — ambiente da disciplina

Sandbox da disciplina **Tópicos Avançados em Engenharia de Software 2** (TEES),
PPgTI/UFRN, 2026.2. Separa as atividades do curso do repositório vivo da tese, e
serve de ambiente de desenvolvimento assistido por IA para o estudo de caso: o
pipeline **M-LRSDI** de modelagem de sinistros rodoviários.

## O que há aqui

- `AGENTS.md` e `CLAUDE.md`: contexto de projeto lido pelos agentes de IA.
- `.mcp.json`: servidores MCP (`sqlite-ouro` em leitura, `fs-lai` em leitura).
- `.claude/settings.json`: permissões do agente (deny, ask, allow).
- `.gitignore`: proteção de dados e segredos.
- `docs/adr/`: ADRs do trabalho, em espelho markdown versionável.

## O que NÃO há aqui

Dados brutos, bancos e o código do pipeline vivem no repositório da tese
(`D:\PPgTI_UFRN\VSCODE\Tese_BR`). Este ambiente os referencia por variável de
ambiente (`TESE_DB`, `LAI_DIR`), sem duplicar nem versionar dados.

## Módulos do trabalho

1. Ambiente e fluxo de trabalho (Atividade Assíncrona 1): concluído neste baseline.
2. SDD da extração da LAI para banco: aguarda o material do professor.
3. Harness e agentes de automação: previsto.

## Configurar o ambiente

```powershell
$env:TESE_DB  = "D:\PPgTI_UFRN\VSCODE\Tese_BR\rebuild\tese_brV02.db"
$env:LAI_DIR  = "D:\PPgTI_UFRN\LAI"
claude mcp list
```
