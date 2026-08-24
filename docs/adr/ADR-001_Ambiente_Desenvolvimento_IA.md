**REGISTRO DE DECISÃO ARQUITETURAL**

**ADR-001 — Adoção de ambiente de desenvolvimento assistido por IA (arquivos de contexto CLAUDE.md/AGENTS.md, permissões e fluxo de trabalho com Git)**

| Campo | Conteúdo |
|---|---|
| Identificador | ADR-001 |
| Título | Adoção de ambiente de desenvolvimento assistido por IA (arquivos de contexto CLAUDE.md/AGENTS.md, permissões e fluxo de trabalho com Git) |
| Status | ACEITO |
| Data | 2026-08-24 |
| Decisor | Flávio Eduardo Batista Moreira (doutorando) |
| Projeto | Ambiente da disciplina Tópicos Avançados em Engenharia de Software 2 (sandbox Tese_BR_TEES); estudo de caso: pipeline M-LRSDI da tese, PPgTI/UFRN-IMD |
| Relaciona-se com | A montante, as convenções da tese: ADR-009 (tese) sobre idioma e ADR-026 (tese) sobre determinismo. A jusante, o ADR-002 (servidores MCP) e os módulos de SDD e de automação do trabalho da disciplina. |
| Substitui / é substituído por | Nada registrado |

*Documento elaborado conforme a prática de Architecture Decision Records (RICHARDS; FORD, 2025). Numeração própria da sandbox da disciplina, independente da numeração da tese.*

# 1. Contexto

O ambiente Tese_BR_TEES é a sandbox da disciplina, separada do repositório vivo da
tese, e tem como estudo de caso o pipeline M-LRSDI de coleta e diagnóstico dos dados
abertos do DNIT e da ANTT. A governança da tese se apoia em cinquenta e dois ADRs,
memoriais de proveniência e a revisão de escrita do ADR-009 (tese), o que já configura
uma prática de desenvolvimento guiado por decisões documentadas. Não havia, contudo,
arquivos que orientassem um agente de IA a operar sob essas convenções. Sem eles, o
agente parte de suposições genéricas a cada sessão e pode contrariar decisões já
tomadas, como a leitura bronze imutável ou o determinismo do parsing de data.

# 2. Decisão

Adotar um ambiente de desenvolvimento assistido por IA, composto de um arquivo de
contexto de projeto, permissões declaradas e um fluxo de trabalho com Git. O contexto é
dividido em `AGENTS.md`, com o conteúdo comum lido por várias ferramentas, e
`CLAUDE.md`, que importa o primeiro com `@AGENTS.md` e acrescenta o que é próprio do
Claude Code. As permissões ficam em `.claude/settings.json`, liberando comandos de
leitura e coleta rápida, exigindo confirmação para push e downloads pesados, e
bloqueando comandos destrutivos e a leitura de segredos. O fluxo de Git prevê branch
dedicada, revisão de diff e commit isolado da configuração.

# 3. Justificativas

Os arquivos de contexto convertem convenções dispersas em instruções que o agente lê
no início de cada sessão, o que traz consistência entre sessões, reduz alucinação ao
substituir suposições por comandos reais do projeto, e acelera o entendimento por um
novo integrante, humano ou agente. A separação entre `AGENTS.md` e `CLAUDE.md` evita
duplicar instruções entre ferramentas. As permissões impõem limites técnicos onde o
texto do contexto apenas orienta, o que protege o repositório de ações destrutivas.

# 4. Alternativas consideradas e rejeitadas

Manter apenas o README foi rejeitado porque o README descreve o projeto para pessoas,
sem o formato que o agente lê automaticamente nem as regras de conduta. Concentrar tudo
em um único `CLAUDE.md` foi rejeitado por acoplar o contexto a uma só ferramenta e por
inflar o arquivo. Confiar somente no texto de contexto, sem permissões, foi rejeitado
porque o contexto orienta, mas não impede um comando destrutivo.

# 5. Consequências

O ambiente passa a ter um fluxo reprodutível de trabalho com IA, versionado e sob
revisão como qualquer arquivo. O custo é a manutenção dos arquivos de contexto, que
precisam acompanhar mudanças estruturais do pipeline. A separação em dois arquivos
exige atenção ao ponto de importação. O ganho é a coerência entre o que o agente faz e
as decisões já registradas nos ADRs da tese.

# 6. Conformidade e verificação

A conformidade se verifica ao rodar o agente na raiz do projeto e confirmar, pelo
comando de contexto, o carregamento dos dois arquivos; ao observar que um prompt de
teste retorna descrição coerente com o README; e ao confirmar que os comandos
bloqueados são de fato recusados. O commit da configuração deve aparecer isolado na
branch dedicada.

# 7. Reversibilidade

A decisão é reversível a baixo custo. A remoção dos arquivos de contexto e de permissões
devolve o repositório ao estado anterior, sem afetar dados, bancos ou o código do
pipeline.

# 8. Relacionados

ADR-002 (servidores MCP). Na tese: ADR-009 (idioma), ADR-010 (bronze imutável), ADR-026
(determinismo) e ADR-052 (notebooks consumidores).
