# Branch dedicada + Pull Request (Atividade Assincrona 1, Etapa 5)
# Rode no PowerShell, a partir da pasta Tese_BR_TEES:
#   cd "D:\PPgTI_UFRN\DISCIPLINAS\2026_2\TÓPICOS AVANÇADOS EM ENGENHARIA DE SOFTWARE 2\Tese_BR_TEES"
#   .\01_branch_e_pr.ps1

$ErrorActionPreference = "Stop"

# 1. Garante a main atualizada
git checkout main
git pull --ff-only

# 2. Cria a branch dedicada
git checkout -b feature/setup-inicial

# 3. Adiciona os novos artefatos (Etapa 3, 4 e regra por escopo)
git add src/ tests/ conftest.py docs/prompts-comparacao.md `
        .claude/rules/notebooks.md README.md .gitattributes

# 4. Commit. A mensagem abaixo foi gerada pela IA a partir do diff e revisada.
git commit -m "feat: adiciona src/tests, comparativo de prompts e regra por escopo

- src/parse_datas.py: parsing deterministico de data (dayfirst=True, ADR-026)
- tests/test_parse_datas.py: 3 testes, todos passando
- docs/prompts-comparacao.md: comparativo prompt fraco x eficaz (Etapa 4)
- .claude/rules/notebooks.md: regra por escopo para notebooks
- README: estrutura e comandos atualizados"

# 5. Publica a branch
git push -u origin feature/setup-inicial

# 6. Abre o Pull Request. Requer o GitHub CLI (gh) autenticado (gh auth login).
#    Se nao tiver o gh, abra o PR pela pagina que o push imprime no terminal.
gh pr create `
  --base main `
  --head feature/setup-inicial `
  --title "Setup inicial: src/tests, comparativo de prompts e regra por escopo" `
  --body "Fecha as etapas 3, 4 e a regra customizada por escopo da Atividade Assincrona 1. Nao precisa de merge; PR aberto para praticar o fluxo de revisao."

# 7. Verificacao
git log --oneline -n 5
gh pr view --web   # abre o PR no navegador (opcional)
