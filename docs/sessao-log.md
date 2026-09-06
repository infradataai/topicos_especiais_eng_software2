# Etapa 3 — Observabilidade e checkpoint humano

## Log da sessão do agente (Assíncrona 3)

Registro das ações do agente durante a atividade, na ordem em que ocorreram. É um log curado das ações e decisões, fiel ao que foi feito; o transcript bruto da sessão pode ser exportado do próprio Claude Code, se a banca pedir o registro completo. Os três pilares de observabilidade da aula aparecem ao longo do fluxo: log/transcript, revisão de diff e checkpoints humanos.

### Etapa 1 — harness e guardrail
- Leitura do `.claude/settings.json` existente (permissões da Assíncrona 1).
- Criação de `.claude/hooks/block_data_commit.py` (hook PreToolUse) e registro da seção `hooks` no `settings.json`.
- Teste do hook com três entradas simuladas: bloqueou `git add rebuild/tese_brV02.db` e `git commit ... concedidos-01-2022.csv` (exit 2); liberou `git add src/lai_loader.py` (exit 0).
- Redação de `docs/harness-etapa1.md` com a comparação dos modos de autonomia.
- Revisão de diff: correção de um stub de `src/lai_validador.py` criado por engano na branch errada antes do commit.
- Commit `139adde` na branch `feature/harness-arquitetura`.

### Etapa 2 — TDD
- Red: `tests/test_analise_outliers.py` escrito antes da implementação; pytest falhou com `ModuleNotFoundError: No module named 'src.analise'`.
- Green: `src/analise.py::detectar_outliers_iqr` implementado; 5 testes passaram; suíte completa em 20 testes.
- Tarefa sem TDD: `nivel_risco` implementada direto; teste posterior `xfail` documentou a lacuna de entrada inválida.
- Commits `0b93de8` (Red) e `6cafff9` (Green), preservando a ordem teste-antes-da-implementação no histórico.

## Checkpoint humano obrigatório

Ponto de parada definido: **antes de qualquer escrita no banco consolidado** (a camada ouro/consolidada do projeto). A escolha se justifica porque essa camada é a fonte de todos os resultados a jusante (EDA, custo social, mapa de trechos críticos), e uma escrita indevida propaga erro silencioso por todo o pipeline. É um ponto de alto risco, no critério da aula de checkpoints por risco.

### Simulação do checkpoint

O agente propôs consolidar os microdados carregados em uma tabela do banco, executando uma carga que escreve no arquivo `.db`. A execução foi interrompida no checkpoint, antes da escrita. A revisão humana conferiu o esquema de destino, o nome da tabela e a idempotência da carga.

Decisão registrada: **aprovar com edição**. A tabela de destino recebeu prefixo de camada (`consolidado_...`) e o conjunto de colunas obrigatórias foi fixado antes de liberar a escrita. O papel humano assumido foi o de **Approver**, no framework de cinco papéis da aula: o humano não executa cada passo, mas aprova o marco de escrita no banco antes de ele ocorrer. Essa fronteira complementa o hook da Etapa 1: o hook impede versionar o dado, o checkpoint impede gravá-lo no banco sem revisão.
