# Atividade Assincrona 2 (SDD) - commits com historico real + Pull Request
# Pre-requisito: fazer o merge do PR #1 (feature/setup-inicial) na main pelo GitHub,
# para que a main tenha o conftest.py e o src/ da Assincrona 1.
#
# Rode no PowerShell, a partir da pasta Tese_BR_TEES:
#   cd "D:\PPgTI_UFRN\DISCIPLINAS\2026_2\TÓPICOS AVANÇADOS EM ENGENHARIA DE SOFTWARE 2\Tese_BR_TEES"
#   .\02_commits_e_pr_sdd.ps1

$ErrorActionPreference = "Stop"

# 1. Parte da main atualizada (ja com a Assincrona 1 mesclada)
git checkout main
git pull --ff-only

# 2. Branch dedicada da Assincrona 2
git checkout -b feature/sdd-lai

# 3. Commits em etapas, para ter historico real do processo SDD

# 3.1 Escopo (Etapa 1)
git add docs/escopo.md
git commit -m "docs(sdd): escopo das 3 funcionalidades da LAI (Etapa 1)"

# 3.2 Spec OpenSpec do carregador, depois o codigo e testes
git add openspec/changes/loader-microdados-lai/
git commit -m "spec(openspec): carregador de microdados da LAI (proposal, spec, design, tasks)"
git add src/lai_loader.py tests/test_lai_loader.py
git commit -m "feat: carregador de microdados da LAI com validacao e idempotencia"

# 3.3 Spec Spec-Kit do validador, depois o codigo e testes
git add .specify/ specs/validador-qualidade-lai/
git commit -m "spec(speckit): validador de qualidade da LAI (constituicao, spec, plan, tasks)"
git add src/lai_validador.py tests/test_lai_validador.py
git commit -m "feat: validador de qualidade dos dados carregados da LAI"

# 3.4 Spec OpenSpec do parser de PDF, depois o codigo e testes
git add openspec/changes/parser-pdf-lai/
git commit -m "spec(openspec): parser de tabela da LAI em PDF (proposal, spec, design, tasks)"
git add src/lai_pdf_parser.py tests/test_lai_pdf_parser.py
git commit -m "feat: parser de tabela de resposta da LAI em PDF"

# 3.5 Checkpoint, comparacao e relatorio
git add docs/checkpoint.md docs/comparacao-sdd.md docs/roteiro-sdd-clis.md docs/relatorio-assincrona-2.md
git commit -m "docs(sdd): checkpoint humano, comparacao OpenSpec x Spec-Kit e relatorio"

# 4. Publica a branch e abre o PR (requer gh autenticado)
git push -u origin feature/sdd-lai
gh pr create --base main --head feature/sdd-lai `
  --title "SDD aplicado a extracao da LAI (3 funcionalidades)" `
  --body "Atividade Assincrona 2. Especificacao via OpenSpec (carregador, parser PDF) e Spec-Kit (validador), com codigo, testes, checkpoint humano e comparacao. Nao precisa de merge."

# 5. Verificacao
git log --oneline -10
pytest -q
