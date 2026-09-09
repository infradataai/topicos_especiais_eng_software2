# Tese_BR_TEES — ambiente da disciplina

Sandbox da disciplina **Tópicos Avançados em Engenharia de Software 2** (TEES),
PPgTI/UFRN, 2026.2. Separa as atividades do curso do repositório vivo da tese, e
serve de ambiente de desenvolvimento assistido por IA para o estudo de caso: o
pipeline **M-LRSDI** de modelagem de sinistros rodoviários.

## O que há aqui

- `AGENTS.md` e `CLAUDE.md`: contexto de projeto lido pelos agentes de IA.
- `.claude/rules/`: regra por escopo (convenção específica para notebooks).
- `.claude/settings.json`: permissões do agente (deny, ask, allow).
- `.mcp.json`: servidores MCP (`sqlite-ouro` em leitura, `fs-lai` em leitura).
- `.gitignore` e `.gitattributes`: proteção de dados e segredos, fim de linha.
- `src/`: camada de aplicação (análise descritiva, consulta web, relatórios, carga da LAI).
- `custo_social_core/`: núcleo de dados do projeto final (ingestão da PRF, custo, SNV,
  exposição, saúde, persistência).
- `scripts/`: pontos de entrada da carga e da execução nacional.
- `dados/consolidado.db`: banco consolidado do piloto, versionado por exceção declarada.
- `tests/`: testes em pytest.
- `docs/adr/`: os 13 ADRs do trabalho, em espelho markdown versionável.
- `openspec/`: onze capacidades especificadas e as mudanças arquivadas.
- `docs/prompts-comparacao.md`: comparativo de prompt fraco x eficaz (Etapa 4).
- `Atividades/`: relatórios das atividades assíncronas em PDF.

## Comandos

```bash
pip install -r requirements.txt
pytest -q          # 106 testes: 30 da aplicação e 76 do núcleo de dados
```

## O que NÃO há aqui

Os arquivos de origem, com 35 GB entre PRF, SNV, RENAEST e DATASUS, ficam fora do
controle de versão. Eles vivem no repositório privado `custo-social-sinistro-BR` e são
reproduzíveis pelos scripts de ingestão. A única exceção versionada é o
`dados/consolidado.db`, com 8,5 MB, para que a demonstração rode em outra máquina.

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
