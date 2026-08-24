<!-- Ambiente da disciplina Topicos Avancados em Eng. de Software 2 (TEES).
     Sandbox separado do repositorio vivo da tese; estudo de caso = pipeline M-LRSDI.
     Dados e bancos permanecem no repositorio da tese, referenciados por variavel de ambiente. -->

# AGENTS.md — Tese_BR (Padrão BR: dados abertos DNIT + ANTT)

Contexto de projeto lido por agentes de IA (Cursor, Codex, Copilot e outros).
O CLAUDE.md importa este arquivo. Prosa em português; código, nomes de arquivo,
de tabela e de coluna em inglês (ADR-009).

## Sobre o projeto

Pipeline de coleta, catalogação e diagnóstico dos dados abertos do DNIT e da ANTT
para compor o banco nacional de rodovias federais, o "Padrão BR", replicando o
"Padrão RN" da tese de doutorado (PPgTI/UFRN). Separa rodovias não concessionadas
(DNIT) das concessionadas (ANTT). Faz parte do framework M-LRSDI (Multilayer Road
Safety Data Intelligence).

Unidade de análise: subtrecho SNV por mês (ADR-017). O SNV é a espinha espacial que
integra seis camadas: sinistros (PRF), exposição/VMDa (PNCT), pavimento funcional
(SGP: IRI, ATR, IGG, ICS), pavimento estrutural (FWD) e geometria (deck HDM).

## Stack

- Python 3. Bibliotecas: pandas, numpy, scipy, sqlite3 (stdlib), openpyxl,
  pdfplumber, scikit-learn, statsmodels, pymannkendall, matplotlib.
- Banco: SQLite (arquivos `.db`). Não há Postgres, DuckDB nem Spark.
- Gerar ADRs em Word usa Node.js (pacote `docx`).

## Comandos

- Instalar deps mínimas de coleta: `pip install openpyxl pdfplumber`
- Catálogo DNIT: `python varredura_dnit.py`
- Catálogo ANTT: `python varredura_antt.py`
- Baixar dados abertos (DNIT + ANTT): `python baixa_abertos_BR.py`
- Baixar PDFs de monitoração das concessões: `python coletor_relatorios_antt.py`
- Triagem estrutural FWD/IRI/IGG: `python extrai_estrutural_triagem.py`
- Construção do banco: notebooks `ETL1 -> ETL2 -> ETL3` (bronze -> prata -> ouro)

## Arquitetura de dados (medalhão)

- Bronze: espelho fiel do CSV de origem, lido como texto (`dtype=str`), sem
  converter, limpar ou filtrar (ADR-010). Conversões e recorte da janela ficam a
  jusante.
- Prata: normalização e junção por unidade (silver B1/B3).
- Ouro: camada determinística consumida pela EDA (`tese_brV02.db`).
- Notebooks consumidores da EDA leem a camada ouro e nunca escrevem no banco
  (ADR-052).

## Convenções

- Idioma: prosa em português, código em inglês (ADR-009).
- Determinismo: parsing de data sempre com `dayfirst=True` (ADR-026); o CSV da PRF
  de 2022 vem em DD/MM e sem isso o resultado muda entre execuções.
- Nomes de banco, tabela e coluna seguem a nomenclatura consagrada da arquitetura
  medalhão; não renomear identificadores sem ADR (migrar banco e consultas juntos).
- Validação: rolling-origin temporal mais hold-out espacial, com dobras congeladas
  tratadas como dados (ADR-021).
- Catálogos `.csv` de metadados são versionados; os dados brutos, não.

## Estrutura

- Scripts de coleta e diagnóstico na raiz (`varredura_*.py`, `baixa_abertos_BR.py`,
  `coletor_relatorios_antt.py`, `extrai_estrutural_triagem.py`).
- Notebooks de ETL e EDA na raiz.
- Catálogos `.csv` versionados (`dnit_recursos.csv`, `manifesto_download_BR.csv` e
  outros).
- Documentos de diagnóstico em `.md` (`Diagnostico_Padrao_BR_DNIT_ANTT.md`,
  `Veredito_dados_abertos_DNIT_ANTT.md`).
- ADRs em `DISCIPLINAS/2026_1/ESTUDO DIRIGIDO 2 - ETL EDA E MODELAGEM (ML E DL)/6. ADRs`.

## Não fazer

- Não commitar dados pesados: `*.db`, `relatorios_antt/` (~9,5 GB), `DNIT_aberto/`,
  `ANTT_aberto/`, `PRF_aberto/`, `estrutural_extraido/`, dumps grandes.
- Não commitar segredos: `.env`, tokens, chaves de API.
- Não reescrever a camada bronze: dados brutos são imutáveis (ADR-010).
- Não renomear tabelas ou colunas sem ADR: quebra reprodutibilidade (ADR-026).
- Não colocar lógica de construção de banco nos notebooks consumidores da EDA.
- Não converter, limpar ou filtrar na leitura bronze; faça a jusante.
