# Proposta — Cálculo do custo social por ocorrência (produto escalar C · M)

## Por quê

A ingestão já entrega o vetor C de cada ocorrência: quantas pessoas por gravidade e quantos veículos por tipo. Falta a etapa que transforma essa contagem em dinheiro, aplicando o vetor M de custos médios padrão do IPEA. Sem ela, o piloto tem a base correta e nenhum resultado.

O cálculo precisa ser explícito em três pontos que a leitura ingênua erra. O vetor M varia com a gravidade da ocorrência, e não com a da vítima, de modo que a mesma vítima leve custa R$ 8.469,44 num acidente com feridos e R$ 8.635,77 num acidente com morto. O semirreboque tem identificador próprio na PRF, mas integra a composição do caminhão, e valorá-lo em separado cobra duas vezes o mesmo veículo. E a atualização monetária tem base única declarada, sob pena de somar reais de anos diferentes.

## O que muda

Adiciona um módulo que aplica o vetor M da Tabela 1 do Texto para Discussão 2565 sobre o vetor C, produzindo o custo de cada ocorrência a preços de junho de 2026. O módulo seleciona a coluna do vetor M pela gravidade da ocorrência, soma os componentes de pessoas, de veículos e o bloco institucional, aplica a regra de composição na contagem de caminhões, e devolve o resultado decomposto por categoria, nas duas leituras previstas: por vítima e por ocorrência.

## Fora de escopo

A ancoragem no segmento do SNV, que pertence ao módulo de referenciamento. A criticidade por exposição e a correção de subregistro, que consomem este resultado a jusante. A substituição de componentes do vetor M por valores observados no SIH, no SAMU e no INSS, que é a variante observada e entra como mudança própria. A imputação da gravidade ausente, registrada como sensibilidade no ADR-008.

## Decisões que governam esta mudança

Os três parâmetros já estão fixados no ADR-008: base monetária de junho de 2026 com deflator 1,884802; gravidade não informada com custo zero e contagem declarada à parte; e mapeamento de veículos com a regra de composição para semirreboque e reboque. A memória de cálculo completa, com as três subtabelas do vetor M e um exemplo trabalhado, está em `docs/memoria-calculo-CM.md`.
