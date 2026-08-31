**Universidade Federal do Rio Grande do Norte — Instituto Metrópole Digital**
**Programa de Pós-Graduação em Tecnologia da Informação**
**Disciplina:** Desenvolvimento de Software com IA · Tópicos Avançados em Engenharia de Software 2
**Professor:** Jean Mário Moreira de Lima
**Aluno:** Flávio Eduardo Batista Moreira

# Relatório — Atividade Assíncrona 2 (De Spec a Código)

**Repositório:** https://github.com/infradataai/topicos_especiais_eng_software2

## 1. Funcionalidades escolhidas e por que são bons casos para SDD

O estudo de caso foi o fio da LAI do pipeline da tese. Escolhi três funcionalidades novas: um carregador de microdados da LAI para SQLite com validação e idempotência; um validador de qualidade dos dados carregados; e um parser de tabela de uma resposta da LAI em PDF. São bons casos para SDD porque têm regras de negócio que um agente não adivinha, como a leitura como texto imutável e a idempotência da carga, e casos de borda concretos, como coluna faltando, arquivo vazio, célula ausente e PDF sem tabela. Cada uma toca código, teste e, no carregador, o esquema do banco, e tem ao menos dois cenários de uso, o que exige especificação antes do código.

## 2. Abordagens de especificação e como se comportaram

Especifiquei o carregador e o parser de PDF com OpenSpec, e o validador com o GitHub Spec-Kit. O OpenSpec organiza cada mudança em uma pasta com proposta, spec em delta, design e tarefas, e coube bem ao trabalho incremental sobre código existente. O Spec-Kit parte de uma constituição de projeto e desce da spec ao plano e às tarefas, o que deu um fluxo mais guiado e amarrou de saída a regra de não escrever no banco. Na prática, a estrutura em delta do OpenSpec foi mais direta para o brownfield, e a constituição do Spec-Kit foi mais forte para impor princípios de arquitetura desde o começo. As três specs viraram testes derivados dos critérios de aceite, e os três módulos passam nesses testes.

## 3. Dificuldade real enfrentada

A dificuldade principal foi conceitual, na fronteira entre a spec e o código. Ao revisar o diff do carregador, percebi que a primeira versão passava no teste de carga simples, mas não garantia a idempotência, porque essa regra estava na especificação e não tinha virado teste. A correção foi tornar a regra explícita, com a restrição `UNIQUE` sobre a linha e o `INSERT OR IGNORE`, e travá-la em um teste de recarga. A lição confirma o princípio da aula: quando um teste falha ou uma regra escapa, a pergunta certa é se a especificação estava completa, porque a spec, e não o código, é a fonte de verdade.

## Checklist de entrega

- `docs/escopo.md` com as funcionalidades e a justificativa: sim.
- Especificação completa, com requisitos, critérios de aceite Given/When/Then e caso de borda próprio, e plano revisado: sim, em OpenSpec e Spec-Kit.
- Registro das ferramentas usadas e por quê: `docs/comparacao-sdd.md`.
- Repositório no GitHub com histórico de commits e Pull Request aberto: sim.
- Relatório final de até uma página: este documento.
