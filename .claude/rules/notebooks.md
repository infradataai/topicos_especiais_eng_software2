---
paths:
  - "notebooks/**/*.ipynb"
  - "**/ETL*.ipynb"
  - "**/EDA*.ipynb"
---
# Regra por escopo — notebooks de ETL e EDA

Aplica-se aos notebooks de construcao de banco e de analise exploratoria.

- Notebooks consumidores da EDA leem a camada ouro e NUNCA escrevem no banco (ADR-052 da tese).
- A leitura da camada bronze e feita como texto imutavel (dtype=str); nao converter, limpar
  ou filtrar na leitura, apenas a jusante (ADR-010 da tese).
- Parsing de data sempre com dayfirst=True (ADR-026 da tese); ver src/parse_datas.py.
- Antes de commitar, limpar as saidas das celulas (nbstripout).
- Nao deixar credenciais nem caminhos absolutos de maquina dentro do notebook.
- Logica reaproveitavel sai do notebook para src/ e e importada de volta.
