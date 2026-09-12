**Universidade Federal do Rio Grande do Norte**
**Instituto Metrópole Digital**
**Programa de Pós-Graduação em Tecnologia da Informação**
**Disciplina:** Tópicos Avançados em Engenharia de Software 2 (Desenv. de Software com IA)
**Professor:** Jean Mário Moreira de Lima
**Alunos:** Flávio Eduardo Batista Moreira e Bruno dos Santos Fernandes da Silva

# Custo social do sinistro em quatro categorias

## Análise dos dados disponíveis, leitura do método do IPEA e proposta de aperfeiçoamento

---

## 1. Objetivo

O objetivo é calcular o custo social do sinistro em quatro categorias compatíveis com a tabela de pessoas da PRF: sem vítimas, com dano material apenas; vítimas leves, com dano material e custos de atendimento médico; vítimas graves, com dano material, atendimento médico e custos previdenciários; e óbitos, com a mesma composição das graves. O cálculo segue a metodologia do IPEA e a aperfeiçoa com dados observados. Ele serve ao piloto do RN, na disciplina, e à escala nacional, no artigo.

Este documento reúne três análises. A primeira inventaria os dados já separados. A segunda lê o método do IPEA nos quatro documentos de referência. A terceira cruza as duas com o objetivo e propõe o método.

## 2. Análise 1: os dados disponíveis

A pasta reúne 954 arquivos e 35 GB, em sete fontes. A PRF traz o extrato do RN, com 35.689 linhas por pessoa, de 2019 a 2024, com as colunas de estado físico, tipo de veículo, idade, sexo e as contagens de ilesos, feridos leves, feridos graves e mortos. O SNV entra pela ancoragem já planejada. O DATASUS traz o SIM completo de 2019 a 2025, por UF, com a extração dos óbitos de transporte (CID-10 V01 a V99) e a divisão entre óbito em estabelecimento de saúde e em via pública. O SIH traz as internações por V01 a V99, por UF, ano e mês. O SAMU traz a produção do SIA por UF e ano, com a quantidade de atendimentos e os procedimentos nomeados pela tabela SIGTAP. O RENAEST traz os sinistros de vias estaduais e municipais de todo o país, com a gravidade da lesão. A pasta de custo social traz as sete versões da planilha de parâmetros, os memoriais e as fontes.

Três achados de qualidade mudam o plano de trabalho.

O primeiro é a duplicação no extrato da PRF. O arquivo vem do conjunto "todas as causas e tipos", que repete a mesma pessoa uma vez para cada combinação de causa e tipo de acidente. Das 35.689 linhas, 18.983 (53,2%) são repetições. O extrato tem 7.989 acidentes distintos e 506 com vítima fatal. A contagem de óbitos linha a linha dá 1.570, e a contagem por acidente dá cerca de 441, uma inflação próxima de 3,6 vezes. O extrato também não traz as colunas `pesid` e `id_veiculo`, que identificam a pessoa e o veículo, o que torna a deduplicação frágil. A correção é reconstruir o extrato do RN a partir dos arquivos anuais nacionais, que trazem essas duas chaves, com a deduplicação por pessoa e por veículo, e incluir o ano de 2025, que existe na fonte e ficou fora do extrato.

O segundo é a ausência de valor monetário nos arquivos observados de saúde. O SIH agregado e o SIH detalhado trazem apenas a contagem de internações, sem o valor da autorização de internação. O SAMU traz a quantidade de atendimentos com o valor total zerado, porque os procedimentos do SAMU entram na tabela SIGTAP sem valor unitário, já que o serviço é custeado por repasse em bloco. O custo hospitalar observado exige uma nova extração do SIH com os campos de valor total, dias de permanência e dias de UTI. O custo pré-hospitalar observado exige a razão entre o repasse de custeio do SAMU e o número de atendimentos.

O terceiro é a ausência do dado previdenciário. O pedido ao INSS pela LAI está em recurso, e nenhum arquivo de benefício por incapacidade com CID V01 a V99 está na pasta. O componente previdenciário fica, por ora, estimado, e entra como observado quando a resposta chegar. O dano material da PRF traz a classe de monta (pequena, média, grande) sem valor em reais.

## 3. Análise 2: o método do IPEA

Os quatro documentos formam uma hierarquia. O Relatório Final de 2006, do IPEA com o DENATRAN e a ANTP, é a pesquisa de campo nas rodovias federais, com 244 páginas, e contém o método completo. O documento de 80 páginas é o resumo dessa pesquisa. O Texto para Discussão 2565, de 2020, atualiza a pesquisa de forma simplificada, aplica os custos médios de 2005 e 2006 corrigidos pelo IPCA sobre a base da PRF de 2014, e gera a tabela de custo médio por acidente que a planilha V07 usa. O sumário executivo é uma página do mesmo TD.

O método tem quatro pilares.

O primeiro é a função aditiva de custo. O custo do acidente é a soma dos custos associados às pessoas, aos veículos, à via e ao ambiente, e às instituições. As pessoas somam os cuidados em saúde (pré-hospitalar, hospitalar e pós-hospitalar), a perda de produção e a remoção. Os veículos somam o dano material, a perda de carga e a remoção com pátio. A via soma os danos à propriedade pública e privada. As instituições somam o atendimento policial e os processos.

O segundo é a decomposição em 40 componentes elementares. Cada acidente é um vetor C de 40 posições, que conta quantas vezes cada componente ocorre: quantos ilesos, feridos leves, feridos graves e mortos, cada um com cinco componentes de custo; quantos automóveis, motocicletas, bicicletas, utilitários, caminhões, ônibus e outros, cada um com dois ou três componentes; e os dois componentes institucionais. O custo do acidente é o produto escalar entre C e o vetor M de custos médios padrão, estimado por pesquisa amostral. Há três vetores M, um para cada gravidade do acidente: sem vítimas, com vítimas e com fatalidade. O princípio é a aditividade sem ganho de escala. A Tabela 1 do TD 2565 é exatamente esse vetor M, a preços de dezembro de 2014.

O terceiro é a perda de produção pelo capital humano. Para ilesos, feridos leves e graves, o valor é a renda mensal da vítima vezes os dias parados divididos por 30, descontado à taxa social de 6% ao ano. Para vítimas fatais, o valor é treze rendas mensais por ano vezes o fator de anuidade sobre a sobrevida esperada, descontado à mesma taxa. Esse componente domina o custo: R$ 335 mil a R$ 433 mil por morto, a preços de 2014, e 43% do custo total das rodovias federais.

O quarto é o tratamento do gasto previdenciário. O relatório o define à parte, como a soma do que a empresa paga nos primeiros quinze dias, do que a previdência paga no afastamento e do que o seguro DPVAT paga. E o exclui da função de custo com a justificativa literal: "Sua inclusão, juntamente com o item perda de produção, implicaria uma dupla contagem." O gasto previdenciário é a forma como a perda de renda é financiada, uma transferência, e o custo social é a perda de produção em si.

O método traz ainda dois elementos que servem ao aperfeiçoamento. A Tabela 29 do relatório compara a classificação de gravidade da PRF no local do acidente com a reclassificação médica posterior, e mostra que uma parte dos feridos leves da PRF era grave, e uma parte dos ilesos era leve. As fórmulas hospitalares vêm do estudo urbano de 2001 e usam o custo por dia de enfermaria e por dia de UTI, que é a estrutura que o SIH observa.

O IPEA declara as próprias limitações. Os custos unitários vêm de uma única amostra de 2005 e 2006, corrigida apenas por IPCA, e o TD 2565 recomenda nova pesquisa amostral. O custo das rodovias estaduais e municipais vem de fatores de correção entre 1,6 e 1,97 aplicados sobre a pesquisa antiga, e a fração municipal usa, nas palavras do relatório, um fator "de forma totalmente arbitrária". Os custos não valorados, como o sofrimento e as sequelas psíquicas, ficam fora, e o relatório afirma que o custo encontrado é sempre menor que o real.

## 4. Análise cruzada: as quatro categorias sobre o modelo aditivo

As quatro categorias pretendidas coincidem com a decomposição secundária do IPEA, que abre as pessoas em ilesos, feridos leves, feridos graves e mortos. A tabela da PRF por pessoa traz o estado físico nessas mesmas classes. O objetivo é alcançável na granularidade máxima do método, acima da média de três classes por acidente que a V07 usa.

O mapa entre as categorias e os componentes é o seguinte. O sinistro sem vítimas recebe os componentes de veículo (dano material, remoção com pátio e perda de carga, por tipo de veículo) e os institucionais. O IPEA atribui um custo pequeno também ao ileso, e a recomendação é manter esse termo, com o subtotal de dano material exibido à parte. A vítima leve recebe a parcela de veículo, os três cuidados em saúde e uma perda de produção curta, pelos dias de afastamento. A vítima grave recebe a parcela de veículo, os cuidados em saúde com o hospitalar dominante, e a perda de produção longa. O óbito recebe a parcela de veículo, cuidados em saúde pequenos, a remoção com translado e a perda de produção sobre a sobrevida esperada, que domina.

O cruzamento impõe uma correção conceitual à categoria "custos previdenciários" dos graves e óbitos. Pelo método do IPEA, o custo social desse bloco é a perda de produção. O benefício do INSS financia parte dessa perda, e somá-lo contaria o mesmo valor duas vezes. A proposta é operacionalizar a categoria como perda de produção, e apresentar o gasto previdenciário observado, quando o INSS responder, ao lado do custo, como decomposição de quem paga. Essa leitura preserva a comparabilidade com o IPEA, evita a dupla contagem e responde à finalidade declarada no checkpoint, a alocação de recursos de saúde e previdência.

O vetor C de cada ocorrência sai da tabela da PRF por pessoa e por veículo. As colunas de estado físico contam as pessoas por gravidade, e a coluna de tipo de veículo, após o mapeamento das categorias da PRF para as sete classes do IPEA, conta os veículos. A classificação do acidente escolhe qual dos três vetores M se aplica. A precondição é a deduplicação por `pesid` e `id_veiculo`, sem a qual o vetor C infla.

A tabela abaixo cruza cada componente do vetor M com a fonte original do IPEA, o dado observado disponível e a ação proposta.

| Componente | Fonte no IPEA (2005-2006) | Observado disponível | Ação |
|---|---|---|---|
| Pré-hospitalar | Fórmula fixa mais custo por km, de 2003 | SAMU: atendimentos por UF e ano, sem valor | Manter o IPEA; substituir pela razão custeio/atendimentos quando extraída |
| Hospitalar | Fórmula urbana de 2001, por dia de enfermaria e de UTI | SIH: só contagem de internações | Extrair valor, dias e UTI do SIH e substituir para graves e óbitos |
| Pós-hospitalar | Vinte pacientes de reabilitação, 2001 | SIA parcial | Manter o IPEA, com sinalização |
| Perda de produção, leves e graves | Renda vezes dias parados, 6% | INSS pendente | Reparametrizar com renda média por UF; substituir os dias pelo INSS quando chegar |
| Perda de produção, mortos | Treze rendas vezes anuidade da sobrevida média, 6% | Idade e sexo por vítima na PRF; tábua de sobrevida do IBGE | Reparametrizar por vítima, com a sobrevida da idade real |
| Remoção e translado | Tabela por faixa de distância, 2005 | Nenhum | Manter o IPEA corrigido por IPCA |
| Dano material por veículo | Amostra por tipo de veículo, 2005 | PRF: classe de monta sem valor | Manter o IPEA por tipo; calibrar pela distribuição de monta observada |
| Institucional e patrimonial | Amostra, 2005 | DNIT pendente | Manter o IPEA |

A gravidade da vítima recebe uma correção de classificação. A Tabela 29 do IPEA dá a matriz entre a classificação da PRF e a médica, e a triangulação entre SIH, RENAEST e PRF da planilha V07 permite estimar a mesma matriz com dado atual. A correção realoca uma fração dos leves para graves. O subregistro de óbitos segue o tratamento já feito na V07, com os cenários de piso, central e teto entre a PRF e o SIM.

## 5. O método proposto

O método mantém o IPEA como estrutura e como âncora, e o aperfeiçoa em três variantes, para que cada ganho seja isolável e auditável.

A primeira variante é a replicação. Aplica o vetor M do TD 2565, corrigido pelo IPCA até a base escolhida, sobre o vetor C de cada ocorrência da PRF de 2019 a 2025, deduplicada. O resultado por vítima e por gravidade é a base de comparação, e a soma por acidente deve reproduzir a ordem de grandeza da Tabela 3 do TD 2565.

A segunda variante é a observada. Substitui, um componente por vez, o valor amostral de 2005 pelo valor observado: o hospitalar pelo SIH com valor e dias, o pré-hospitalar pelo custeio do SAMU por atendimento, o previdenciário pelo INSS quando disponível. Cada substituição é registrada como parâmetro, com a fonte e o ano, e a diferença em relação à replicação é o ganho medido do aperfeiçoamento.

A terceira variante é a atuarial. Recalcula a perda de produção de cada morto com a idade e o sexo da vítima na PRF, a tábua de sobrevida do IBGE do ano e a renda média por UF, em vez da sobrevida e da renda médias da amostra de 2005. É a mudança de maior efeito, porque o componente domina o custo e a idade das vítimas varia muito.

Quatro regras valem para as três variantes. A base monetária é única: cada componente observado é tomado a preços do ano e trazido à base por IPCA, para somar com os componentes do IPEA. A classificação de gravidade recebe a correção da matriz. O óbito recebe os cenários de subregistro. A incerteza se propaga: o IPEA publica o intervalo de confiança de cada componente, e a propagação por reamostragem dá a faixa do custo por segmento.

## 6. Recomendações

Para o piloto do RN, no prazo da disciplina, a recomendação é implementar a replicação completa e uma substituição observada. A replicação é rápida, porque o vetor M já existe na Tabela 1 e o vetor C sai da PRF deduplicada, e é defensável na banca por reproduzir o método oficial. A substituição escolhida é o hospitalar pelo SIH, porque é o segundo maior componente e o dado está a uma extração de distância. A variante atuarial entra se o tempo permitir, porque a idade já está na PRF. O mapa mostra o custo por segmento nas quatro categorias, com a leitura por quilômetro e por exposição, e com a faixa de subregistro.

Para o artigo nacional, a recomendação é o programa completo. A replicação do IPEA com a PRF de 2019 a 2025 por vítima é a primeira estimativa nacional nessa granularidade desde 2014. As substituições observadas respondem à recomendação do próprio TD 2565 de renovar os custos unitários. A variante atuarial corrige o componente dominante. O RENAEST substitui os fatores de 1,6 a 1,97 e a fração arbitrária das rodovias estaduais e municipais por uma estimativa de baixo para cima. A decomposição de quem paga, com o INSS e o SUS, dá ao artigo a leitura de política pública. A análise de sensibilidade cobre a taxa de desconto (6% do IPEA contra 3% e 5%), a matriz de reclassificação e o subregistro. O cenário de custo por vida, já presente na V07, entra como comparação com a abordagem de disposição a pagar, que o IPEA discute e não adota.

## 7. Ações imediatas sobre os dados

A primeira ação é reconstruir o extrato do RN a partir dos arquivos anuais nacionais da PRF, de 2019 a 2025, com `pesid` e `id_veiculo`, e deduplicar por pessoa e por veículo. A segunda é extrair do SIH os campos de valor total, dias de permanência e dias de UTI para as internações V01 a V99, por UF e ano. A terceira é obter o repasse de custeio do SAMU por UF e ano para compor o custo por atendimento. A quarta é mapear as categorias de tipo de veículo da PRF para as sete classes do IPEA. A quinta é obter a tábua de sobrevida do IBGE e a renda média por UF para a variante atuarial. A sexta é manter a reserva do INSS pronta para a chegada da resposta.

## 8. Riscos e limites

A deduplicação da PRF é a precondição de tudo, e um erro nela contamina o vetor C e o custo. A substituição de componentes por dado observado exige uma base monetária única, sob risco de somar reais de anos diferentes. O gasto previdenciário nunca entra como parcela adicional, sob pena de dupla contagem. Os custos não valorados ficam fora, e o resultado é um piso, como o IPEA adverte. O prazo da disciplina limita o piloto à replicação e a uma substituição; o restante fica documentado como parâmetro para o artigo.
