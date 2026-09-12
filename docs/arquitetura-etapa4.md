# Etapa 4 — Revisão arquitetural com apoio de IA

## Resumo da arquitetura atual (a partir do código real)

O projeto é um monólito modular: um único repositório e um pacote `src/`, dividido em módulos pequenos de responsabilidade única. O resumo abaixo foi levantado a partir do código, dos imports de cada módulo e do acoplamento teste a módulo.

| Módulo | Responsabilidade | Dependências |
|---|---|---|
| `src/parse_datas.py` | Parsing determinístico de datas (dayfirst) | pandas |
| `src/lai_loader.py` | Carga de microdados da LAI para SQLite (idempotente) | pandas, sqlite3, hashlib, pathlib |
| `src/lai_validador.py` | Validação de qualidade e contagem de linhas | sqlite3 |
| `src/lai_pdf_parser.py` | Extração de tabela de PDF (lógica pura + wrapper) | pathlib, pdfplumber (lazy) |
| `src/analise.py` | Estatística de apoio (outliers IQR, nível de risco) | statistics |

## Dependências e pontos de acoplamento

O achado principal é a ausência de acoplamento interno: nenhum módulo de `src/` importa outro. Cada um depende apenas de bibliotecas externas, e cada arquivo de teste importa um único módulo. O acoplamento existente é com contratos implícitos, não com código: vários módulos recebem uma conexão SQLite (`con`) como parâmetro, e compartilham convenções do projeto (leitura como texto na camada bronze, coluna técnica `_row_hash` para idempotência). Esses contratos hoje vivem no código e na documentação, não em tipos explícitos.

## Decisão arquitetural

O projeto **está no tamanho certo** e deve permanecer um monólito modular. Não se justifica extrair um serviço nem fragmentar em mais camadas neste momento.

A justificativa se apoia nos critérios da aula, não em opinião. Primeiro, o acoplamento já é mínimo (zero entre módulos) e a coesão é alta (uma responsabilidade por módulo), que são exatamente as metas que a extração de serviços busca alcançar; extrair aqui resolveria um problema que não existe. Segundo, o dado recente favorece o monólito modular como ponto de partida: um agente de IA raciocina melhor com a lógica co-localizada, e o custo operacional de microserviços (deploys, contratos de rede, observabilidade distribuída) não se paga para cinco módulos pequenos. Terceiro, a regra prática é extrair serviço só para dois a cinco pontos quentes reais (alta escala, times distintos, isolamento), e o projeto não tem nenhum.

A melhoria de baixo custo que faz sentido, sem virar serviço, é tornar explícito o contrato de conexão com o banco: um módulo fino de acesso a dados que centralize a abertura da conexão SQLite e as convenções da camada bronze, transformando o contrato hoje implícito em interface declarada. Isso aumenta a modularidade sem introduzir a complexidade de um serviço separado, e prepara o terreno para a troca futura de SQLite por DuckDB/PostgreSQL quando o projeto escalar para o Brasil.
