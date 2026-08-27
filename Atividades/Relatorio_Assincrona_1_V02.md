**Universidade Federal do Rio Grande do Norte**

**Instituto Metrópole Digital**

**Programa de Pós-Graduação em Tecnologia da Informação**

**Disciplina:** Tópicos Avançados em Engenharia de Software 2 (Desenv.de Software com IA)

**Professor:** Jean Mário Moreira de Lima

**Aluno:** Flávio Eduardo Batista Moreira

# Relatório — Atividade Assíncrona 1

**Repositório:** https://github.com/infradataai/topicos_especiais_eng_software2

## 1. Ferramenta configurada e por quê

Foi configurado no Claude Code, um agente de terminal da categoria *CLI agent*, complementado pela leitura interoperável do contexto por um editor com assistente. A escolha atende à *stack* do trabalho, Python com SQLite, e à necessidade de um agente que leia a base, rode *scripts* e proponha mudanças sob revisão, mantendo os dados na máquina local.

## 2. Trecho mais útil do arquivo de contexto

O trecho mais útil do `AGENTS.md` é a seção de restrições, porque impede erros caros de forma verificável:

    ## Não fazer
    - Não commitar dados pesados nem segredos.
    - Não reescrever a camada bronze: dados brutos são imutáveis.
    - Não renomear tabelas ou colunas sem ADR: quebra reprodutibilidade.
    - Parsing de data sempre com dayfirst=True (determinismo).

É o mais útil porque converte decisões de arquitetura já registradas em regras que o agente lê a cada sessão, o que evita que ele contrarie o determinismo do projeto ou versione dados que não devem entrar no repositório, e principalmente não modificar o DB da camada bronze.

## 3. Diferença entre o prompt fraco e o eficaz

A funcionalidade escolhida foi uma função de *parsing* de datas do CSV da PRF. O prompt fraco (“faça uma função que converte datas”) gerou código que roda, mas sem `dayfirst=True`, o que torna a leitura dependente do ambiente e faz a mesma data variar entre máquinas. O prompt eficaz declarou contexto, padrão a seguir, restrições e forma de validar, e produziu uma função determinística, sem efeito colateral, com tratamento de erro e teste que passa. A qualidade seguiu a qualidade do contexto, não a capacidade bruta do modelo. O comparativo completo está em `docs/prompts-comparacao.md`.

## 4. Obstáculo enfrentado e solução

O obstáculo principal apareceu na inicialização do Git dentro do ambiente de trabalho, que deixou arquivos de trava no diretório `.git` e impedia novos comandos. A solução foi isolar o baseline em um *script PowerShell* que remove qualquer `.git` incompleto e reinicializa o repositório de forma limpa, na *branch* principal, antes de conectar ao GitHub e enviar. O mesmo cuidado guiou o `.gitattributes`, que normaliza o fim de linha entre sistemas e encerrou os avisos de conversão.

## Checklist de entrega

  - Repositório no GitHub com histórico de commits: sim.
  - `AGENTS.md`/`CLAUDE.md` e ao menos uma regra customizada por escopo (`.claude/rules/notebooks.md`): sim.
  - Estrutura organizada, `README.md` e ADR em `docs/adr/` (ADR-001 e ADR-002): sim.
  - `docs/prompts-comparacao.md` com o comparativo de prompts: sim.
  - Pull Request aberto (branch `feature/setup-inicial`): sim.
  - `.mcp.json` com dois servidores: sim.
  - Relatório final: este documento: sim
