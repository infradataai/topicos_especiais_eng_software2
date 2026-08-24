**REGISTRO DE DECISÃO ARQUITETURAL**

**ADR-054 — Servidores MCP e fronteiras de acesso (consulta em leitura à camada ouro e leitura da pasta LAI)**

| Campo | Conteúdo |
|---|---|
| Identificador | ADR-054 |
| Título | Servidores MCP e fronteiras de acesso (consulta em leitura à camada ouro e leitura da pasta LAI) |
| Status | ACEITO (documentar); homologação do orientador pendente |
| Data | 2026-08-24 |
| Decisor | Flávio Eduardo Batista Moreira (doutorando); Prof. Elias Jacob de Menezes Neto (homologação pendente) |
| Projeto | Modelagem espaço-temporal multifatorial de sinistros rodoviários com integração de pavimento estrutural e risco ajustado por exposição, PPgTI/UFRN-IMD |
| Relaciona-se com | A montante, o ADR-053 (ambiente de IA). A jusante, o agente de qualidade de dados e o agente de acompanhamento da LAI, previstos no módulo de automação. |
| Substitui / é substituído por | Nada registrado |

*Documento elaborado conforme a prática de Architecture Decision Records (RICHARDS; FORD, 2025), no âmbito do protocolo reprodutível da tese (CRISP-DM, fase Data Preparation).*

# 1. Contexto

O ambiente de IA adotado no ADR-053 permite conectar o agente a ferramentas externas
pelo Model Context Protocol. Duas necessidades do projeto se beneficiam disso: consultar
a camada ouro durante a EDA, hoje feita abrindo o banco à mão, e acompanhar os oito
pedidos da LAI, hoje rastreados em um arquivo de controle. Cada servidor conectado, no
entanto, amplia a superfície de risco e consome contexto com definições de ferramenta,
o que exige um critério de parcimônia.

# 2. Decisão

Declarar, no `.mcp.json` do projeto, apenas dois servidores. O `sqlite-ouro` consulta a
camada ouro (`tese_brV02.db`) em leitura, para perguntas sobre a EDA em linguagem
natural. O `fs-lai` dá acesso de leitura à pasta `LAI`. Os caminhos sensíveis usam
variáveis de ambiente, sem gravar valores no arquivo versionado. Ambos os servidores
exigem aprovação na primeira sessão por virem do `.mcp.json`.

# 3. Justificativas

A conexão da camada ouro em leitura habilita consulta em linguagem natural sem risco de
escrita acidental no banco, o que preserva o determinismo do ADR-026. O acesso de leitura
à pasta `LAI` prepara o agente de acompanhamento sem conceder escrita. Manter apenas dois
servidores segue o critério de conectar somente o necessário, reduzindo superfície de
ataque e gasto de contexto. O uso de variáveis de ambiente evita expor caminhos e
segredos no arquivo versionado.

# 4. Alternativas consideradas e rejeitadas

Conectar um servidor com escrita no banco foi rejeitado porque contraria o determinismo e
a imutabilidade das camadas. Expor o repositório inteiro no servidor de filesystem foi
rejeitado pelo princípio do menor privilégio. Gravar caminhos e tokens diretamente no
`.mcp.json` foi rejeitado por expor dados sensíveis no arquivo versionado. Adicionar
servidores de banco de dados externos foi rejeitado porque a stack é local, em SQLite.

# 5. Consequências

O agente passa a consultar a camada ouro e a ler a pasta `LAI` de forma controlada. O
custo é a necessidade de aprovar os servidores e de manter as variáveis de ambiente
definidas na sessão. A restrição a leitura impede que o agente altere o banco ou os dados
da LAI, o que exige que qualquer escrita passe por código revisado, e não pelo MCP.

# 6. Conformidade e verificação

A conformidade se verifica com o comando que lista os servidores MCP, que deve mostrar os
dois conectados; com um prompt que liste as tabelas da camada ouro; e com a confirmação de
que nenhuma operação de escrita é oferecida pelos servidores declarados.

# 7. Reversibilidade

A decisão é reversível. A remoção de uma entrada do `.mcp.json` desconecta o servidor
correspondente sem afetar dados nem código.

# 8. Relacionados

ADR-053 (ambiente de IA), ADR-010 (bronze imutável), ADR-026 (determinismo) e ADR-041
(custo social, consumidor a jusante dos dados da LAI).
