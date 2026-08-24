# Baseline de Git do ambiente Tese_BR_TEES (Atividade Assincrona 1)
# Rode no PowerShell, a partir desta pasta:
#   cd "D:\PPgTI_UFRN\DISCIPLINAS\2026_2\TÓPICOS AVANÇADOS EM ENGENHARIA DE SOFTWARE 2\Tese_BR_TEES"
#   .\00_baseline_git.ps1

$ErrorActionPreference = "Stop"
$Remote = "https://github.com/infradataai/topicos_especiais_eng_software2.git"

# 1. Remove qualquer .git incompleto deixado pelo ambiente
if (Test-Path ".git") {
    Write-Host "Removendo .git incompleto..."
    Remove-Item -Recurse -Force ".git"
}

# 2. Inicializa o repositorio na branch main
git init -b main
git config user.email "eemoreira@gmail.com"
git config user.name  "Flavio Eduardo Batista Moreira"

# 3. Primeiro commit (baseline do ambiente de IA)
git add -A
git commit -m "chore: baseline do ambiente de desenvolvimento assistido por IA (Assincrona 1)"

# 4. Conecta ao repositorio remoto e envia
git remote add origin $Remote
git push -u origin main

# 5. Verificacao
git log --oneline
git remote -v
Write-Host "`nBaseline concluido. Arquivos versionados:"
git ls-files
