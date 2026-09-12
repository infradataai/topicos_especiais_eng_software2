# ADR-010 — Repositório privado como fonte única do núcleo e ambiente de trabalho

Formato MADR. Numeração própria da sandbox da disciplina.

- Status: SUBSTITUÍDO pelo ADR-013, em 2026-09-09
- Data: 2026-09-07
- Decisores: Flávio Eduardo Batista Moreira e Bruno dos Santos Fernandes da Silva
- Relaciona-se com: ADR-004 (topologia de repositórios), que este ADR revisa em parte
- Substituído por: ADR-013 (consolidação do trabalho no repositório da disciplina)
- Supersede: a cláusula do ADR-004 que fixava o repositório público como fonte única do núcleo

## Contexto

O ADR-004 decidiu que o núcleo de cálculo seria escrito no repositório público da disciplina e que o repositório privado consumiria uma cópia controlada. A decisão fazia sentido enquanto o piloto era o único trabalho em curso e não havia dado carregado.

Três fatos mudaram desde então. Os dados vivem no repositório privado, com 35 GB em sete fontes, e a ingestão só executa onde eles estão. A dupla e os dois professores têm acesso ao repositório privado, o que o torna o lugar natural da colaboração. E a especificação do projeto final admite repositório fechado, desde que o acesso seja concedido ao professor, o que já ocorreu.

Manter a fonte do núcleo separada do lugar onde ele roda passou a custar uma sincronização manual a cada mudança, com risco de divergência entre as duas cópias, que é justamente o que o ADR-003 manda evitar.

## Decisão

O repositório privado `custo-social-sinistro-BR` passa a ser a fonte única do núcleo e o ambiente de trabalho da dupla. Nele ficam o pacote `custo_social_core`, os scripts, os testes, os ADRs, o pacote OpenSpec, os documentos de análise e a pasta de dados, que segue fora do controle de versão.

O repositório público da disciplina, `topicos_especiais_eng_software2`, mantém o histórico das três atividades assíncronas e recebe os entregáveis do projeto final que forem de leitura pública. Ele deixa de ser a fonte do núcleo.

O pacote passa a ficar na raiz do repositório privado, e não sob uma pasta de projeto, o que encurta o caminho de importação.

## Alternativas consideradas

**Manter o ADR-004 como está.** Preservaria a decisão anterior ao custo de sincronizar duas cópias a cada mudança do núcleo. Descartada porque a divergência entre cópias é o risco que a arquitetura procura evitar.

**Promover o núcleo a pacote público independente, importado pelos dois.** Resolve a duplicação e continua sendo a evolução natural quando o projeto crescer. Descartada agora por acrescentar uma etapa de empacotamento e um terceiro repositório, sem ganho no prazo corrente.

**Levar os dados para o repositório público.** Inviável, porque parte das fontes tem dado pessoal e o volume não cabe no controle de versão.

## Consequências

Ganha-se uma fonte única, sem sincronização manual, e o código passa a viver onde os dados estão, o que elimina o descolamento entre desenvolver e executar. A colaboração dos quatro integrantes acontece num só lugar, com histórico de commits contínuo.

Perde-se a visibilidade pública imediata do núcleo. O acesso do professor está concedido, o que atende à especificação, mas a leitura por terceiros passa a depender de convite. Os entregáveis do projeto final que forem públicos precisam ser copiados para o repositório da disciplina, e essa cópia passa a ser a exceção controlada, no sentido inverso ao do ADR-004.

Assume-se a dívida de decidir, ao fim da disciplina, o que do núcleo se torna público, seja pela promoção a pacote próprio, seja pela abertura do repositório.

## Reversibilidade

Alta. O conteúdo é o mesmo nos dois lados hoje, e voltar a fonte para o repositório público significa copiar as pastas de volta e ajustar o caminho de importação, sem migração de dado nem perda de histórico.
