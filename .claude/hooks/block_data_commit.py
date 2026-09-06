#!/usr/bin/env python3
"""Hook PreToolUse (Claude Code) — bloqueia versionar arquivos de dados.

Risco do projeto: os microdados da PRF e da LAI contem dados pessoais, e os
bancos sao pesados. Versiona-los por engano vaza dado sensivel e incha o repo.
Este hook inspeciona comandos Bash e bloqueia (exit 2) qualquer 'git add' ou
'git commit' que referencie extensoes de dados. Complementa o .gitignore:
o .gitignore evita o 'git add .'; este hook barra a inclusao explicita.
"""
import json
import re
import sys

EXTS = (".db", ".sqlite", ".sqlite3", ".csv", ".xlsx", ".xls", ".parquet")

def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # sem payload valido, nao interfere
    cmd = (payload.get("tool_input", {}) or {}).get("command", "")
    if not cmd:
        sys.exit(0)
    if re.search(r"\bgit\s+(add|commit)\b", cmd) and any(e in cmd.lower() for e in EXTS):
        sys.stderr.write(
            "BLOQUEADO pelo hook block_data_commit: o comando tenta versionar um "
            "arquivo de dados (.db/.csv/.xlsx/...). Esses dados contem informacao "
            "pessoal (BATs/LAI) e nao devem entrar no repositorio. Use o .gitignore "
            "ou mova o dado para fora do controle de versao.\n"
        )
        sys.exit(2)  # exit 2 bloqueia a acao no Claude Code
    sys.exit(0)

if __name__ == "__main__":
    main()
