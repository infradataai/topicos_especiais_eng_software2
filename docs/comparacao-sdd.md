# Comparação de abordagens de SDD: OpenSpec e Spec-Kit

A funcionalidade 1 (carregador) e a funcionalidade 3 (parser de PDF) foram especificadas com OpenSpec; a funcionalidade 2 (validador) foi especificada com o GitHub Spec-Kit. O objetivo foi comparar as duas abordagens sobre o mesmo tipo de problema.

## Artefatos gerados

O OpenSpec organiza cada mudança em uma pasta própria em `openspec/changes/`, com quatro artefatos: `proposal.md` com o porquê e o que muda, `specs/` com a spec em delta (seções ADDED, MODIFIED, REMOVED), `design.md` com as decisões e alternativas, e `tasks.md` com a lista de tarefas. O Spec-Kit organiza a funcionalidade em `specs/<feature>/`, com `spec.md`, `plan.md` e `tasks.md`, mais uma constituição de projeto em `.specify/memory/constitution.md`, que fixa princípios globais.

## Estratégias de especificação

O OpenSpec favorece o trabalho incremental sobre código existente, porque a spec em delta descreve apenas o que muda, o que evita reescrever a especificação inteira a cada ajuste. O Spec-Kit parte de uma constituição que vale para o projeto todo e desce da spec ao plano técnico e às tarefas, o que dá um fluxo mais guiado e uniforme. Na prática, a estrutura em delta do OpenSpec coube melhor no parser de PDF, uma extensão da ingestão já existente; a constituição do Spec-Kit ajudou o validador, ao amarrar de saída a regra de não escrever no banco.

## Pontos positivos e negativos

O OpenSpec tem entrada baixa e vive inteiro no repositório, sem serviço externo, mas deixa a cargo do autor manter a coerência entre as pastas de mudança. O Spec-Kit traz o benefício da constituição e de comandos em sequência que padronizam o fluxo, ao custo de mais etapas e de uma curva um pouco maior. Para um projeto de dados pequeno e brownfield como este, o OpenSpec foi mais direto; para impor princípios de arquitetura desde o início, o Spec-Kit foi mais forte.

## Código gerado

Os três módulos atendem aos requisitos das respectivas specs e passam nos testes derivados dos critérios de aceite. A arquitetura ficou coerente entre as abordagens, porque as decisões estruturais (leitura como texto, idempotência, separação entre leitura de PDF e normalização, ausência de escrita no validador) foram fixadas nas specs antes do código, e não deixadas para o agente decidir na geração.
