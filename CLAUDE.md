@AGENTS.md

# CLAUDE.md — específico do Claude Code

O contexto geral do projeto está no AGENTS.md, importado acima. Esta seção traz
apenas o que é próprio do Claude Code.

## Fluxo de trabalho

- Use plan mode antes de qualquer mudança que toque os notebooks de ETL ou a
  construção de banco. Mapeie os arquivos afetados antes de editar.
- Antes de propor um commit, rode a verificação disponível e relate o resultado.
- Trabalhe sempre em branch dedicada; nunca edite direto na `main`.

## Servidores MCP

- `sqlite-ouro`: consulta a camada ouro (`tese_brV02.db`) em modo leitura, para
  perguntas sobre a EDA. Não use para escrever no banco.
- `fs-lai`: acesso de leitura à pasta `LAI`, para o acompanhamento dos pedidos.

## Regras por escopo

- Notebooks: são para exploração e construção documentada, não para lógica
  reaproveitável solta. Limpe as saídas antes de commitar.
- Scripts de coleta (`varredura_*`, `baixa_*`, `coletor_*`): são retomáveis; não
  reescreva a lógica de retomada sem necessidade.

<!-- Mantenedor: manter este arquivo abaixo de ~200 linhas; detalhe fica no AGENTS.md. -->
