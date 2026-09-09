**Universidade Federal do Rio Grande do Norte**
**Instituto Metrópole Digital**
**Programa de Pós-Graduação em Tecnologia da Informação**
**Disciplina:** Tópicos Avançados em Engenharia de Software 2 (Desenv. de Software com IA)
**Professor:** Jean Mário Moreira de Lima
**Alunos:** Flávio Eduardo Batista Moreira e Bruno dos Santos Fernandes da Silva

# Memória de cálculo do custo social por ocorrência

## O produto escalar C · M, do microdado da PRF às quatro categorias por vítima

---

## 1. A fórmula

O IPEA define o custo de um sinistro como a soma dos custos médios de cada componente elementar presente naquela ocorrência, sem ganho de escala. O relatório de 2006 formaliza a decomposição em quarenta componentes e escreve o custo como o produto escalar entre dois vetores:

    custo(i) = C(i) · M(s)

O vetor **C(i)** conta, na ocorrência *i*, quantas vezes cada componente aparece: quantas pessoas de cada gravidade e quantos veículos de cada classe. O vetor **M(s)** traz o custo médio padrão de cada componente, e varia com a gravidade *s* da ocorrência, não da vítima. Há três vetores M: um para o acidente sem vítimas, um para o acidente com vítimas e um para o acidente com fatalidade.

A distinção entre a gravidade da ocorrência e a gravidade da vítima é a chave do método, e costuma ser o ponto de confusão. Uma vítima de lesão leve custa R$ 8.469,44 quando está num acidente com vítimas, e R$ 8.635,77 quando está num acidente que teve um morto. O mesmo componente elementar tem preço diferente conforme a gravidade do evento em que ocorreu.

## 2. O vetor M, da Tabela 1 do TD 2565

Os valores estão a preços de dezembro de 2014. As três subtabelas abaixo reproduzem a Tabela 1 do Texto para Discussão 2565.

### 2.1 Componentes associados às pessoas (Tabela 1A)

| Gravidade da vítima | Componente | Sem vítimas | Com vítimas | Com fatalidade |
|---|---|---:|---:|---:|
| Ilesos | Pré-hospitalares | 4,42 | 414,44 | 0,00 |
| | Hospitalares | 625,60 | 675,59 | 68,57 |
| | Pós-hospitalares | 40,59 | 0,00 | 352,78 |
| | Perda de produção | 415,53 | 3.020,57 | 1.418,60 |
| | **Total** | **1.086,14** | **4.110,60** | **1.839,94** |
| Feridos leves | Pré-hospitalares | 0,00 | 759,18 | 3.488,81 |
| | Hospitalares | 620,62 | 5.661,76 | 1.969,46 |
| | Pós-hospitalares | 0,00 | 208,50 | 1.528,73 |
| | Perda de produção | 5.835,71 | 1.840,00 | 1.648,76 |
| | **Total** | **6.456,33** | **8.469,44** | **8.635,77** |
| Feridos graves | Pré-hospitalares | 1.707,32 | 1.111,73 | 1.032,95 |
| | Hospitalares | 18.069,70 | 72.855,40 | 56.862,42 |
| | Pós-hospitalares | 160,13 | 3.150,21 | 5.498,02 |
| | Perda de produção | 2.483,92 | 47.797,94 | 77.113,46 |
| | Remoção | – | 218,64 | 649,12 |
| | **Total** | **22.421,06** | **125.133,91** | **141.155,96** |
| Mortos | Pré-hospitalares | – | 0,00 | 86,28 |
| | Hospitalares | – | 0,00 | 143,19 |
| | Pós-hospitalares | – | 0,00 | 0,00 |
| | Perda de produção | – | 335.172,20 | 432.557,99 |
| | Remoção | 199,28 | – | 499,24 |
| | **Total** | **199,28** | **335.172,20** | **433.286,69** |

O IPEA anota que a vítima classificada como ilesa ainda incorre em custo, por atendimento posterior, afastamento do trabalho ou falecimento após a classificação do agente no local.

### 2.2 Componentes associados aos veículos (Tabela 1B)

| Classe do veículo | Componente | Sem vítimas | Com vítimas | Com fatalidade |
|---|---|---:|---:|---:|
| Automóveis | Remoção e pátio | 193,22 | 168,10 | 743,60 |
| | Danos materiais | 6.965,90 | 11.958,72 | 18.580,31 |
| | **Total** | **7.159,12** | **12.126,82** | **19.323,91** |
| Motocicletas | Remoção e pátio | 51,59 | 145,28 | 181,09 |
| | Danos materiais | 2.421,61 | 2.595,74 | 4.088,74 |
| | **Total** | **2.473,21** | **2.741,02** | **4.269,83** |
| Bicicletas | **Total** | – | **168,74** | **124,10** |
| Utilitários | Remoção e pátio | 110,76 | 162,96 | 127,14 |
| | Danos materiais | 10.396,71 | 19.846,39 | 34.861,81 |
| | Perda de carga | 62,29 | 231,03 | 102,51 |
| | **Total** | **10.569,76** | **20.240,38** | **35.091,47** |
| Caminhões | Remoção e pátio | 178,33 | 351,53 | 461,89 |
| | Danos materiais | 18.805,75 | 57.009,43 | 41.718,38 |
| | Perda de carga | 3.329,84 | 8.295,05 | 5.645,19 |
| | **Total** | **22.313,92** | **65.656,00** | **47.825,45** |
| Ônibus | Remoção e pátio | 64,39 | 218,46 | 522,97 |
| | Danos materiais | 16.004,91 | 10.318,39 | 20.163,12 |
| | **Total** | **16.069,30** | **10.536,86** | **20.686,09** |
| Outros | Remoção e pátio | 88,52 | 177,05 | 1.403,74 |
| | Danos materiais | 10.218,84 | 79.931,58 | 52.522,13 |
| | Perda de carga | 0,00 | 0,00 | 27.283,43 |
| | **Total** | **10.307,36** | **80.108,63** | **81.209,29** |

### 2.3 Componentes institucionais e patrimoniais (Tabela 1C)

| Componente | Sem vítimas | Com vítimas | Com fatalidade |
|---|---:|---:|---:|
| Atendimento | 151,94 | 238,22 | 342,96 |
| Danos patrimoniais | 301,41 | 100,11 | 310,10 |
| **Total** | **453,35** | **338,33** | **653,06** |

Este bloco entra uma vez por ocorrência, independentemente do número de vítimas ou de veículos.

## 3. A atualização monetária

Os valores da Tabela 1 estão em dezembro de 2014 e são trazidos para junho de 2026 pelo IPCA acumulado. O fator é o produto dos fatores anuais de 2015 a 2026, com 2026 parcial até junho:

    deflator = 1,1067 × 1,0629 × 1,0295 × 1,0375 × 1,0431 × 1,0452
             × 1,1006 × 1,0578 × 1,0462 × 1,0483 × 1,0426 × 1,0336
             = 1,884802

A conferência fecha com o parâmetro já adotado na planilha V07: 23.498,77 × 1,884802 = 44.290,53, que é o custo do acidente sem vítimas a preços de junho de 2026. A base monetária de junho de 2026 fica fixada, o que preserva a comparabilidade com o ensaio nacional já feito.

## 4. O vetor C, a partir do microdado

O vetor C sai das tabelas normalizadas produzidas pela ingestão. A contagem de pessoas por gravidade vem da tabela de pessoas, deduplicada por `(id, pesid)`, no campo de gravidade derivado do estado físico. A contagem de veículos por classe vem da tabela de veículos, deduplicada por `(id, id_veiculo)`, com o tipo da PRF mapeado para as sete classes do IPEA. A gravidade da ocorrência, que escolhe qual dos três vetores M se aplica, vem do campo de classificação do acidente.

O mapeamento dos vinte e dois tipos de veículo observados no Rio Grande do Norte para as sete classes do IPEA é o seguinte.

| Classe do IPEA | Tipos da PRF | Veículos no RN |
|---|---|---:|
| Automóveis | Automóvel | 6.367 |
| Motocicletas | Motocicleta, Motoneta, Ciclomotor, Triciclo, Quadriciclo | 6.690 |
| Bicicletas | Bicicleta | 391 |
| Utilitários | Caminhonete, Camioneta, Utilitário | 2.054 |
| Caminhões | Caminhão, Caminhão-trator | 1.410 |
| Ônibus | Ônibus, Micro-ônibus | 355 |
| Outros | Carroça-charrete, Trator de rodas, Motor-casa, Carro de mão, Trem-bonde, Outros | 135 |
| Regra de composição | Semirreboque, Reboque | 614 |

A última linha não é uma classe, e sim uma regra. O semirreboque e o reboque não recebem valor próprio: eles integram a composição da unidade tratora que os puxa. A contagem de caminhões de cada ocorrência segue a regra

    n_caminhões(i) = n_tratoras(i),                     se n_tratoras(i) > 0
    n_caminhões(i) = 1,                                 se n_tratoras(i) = 0 e há carreta
    n_caminhões(i) = 0,                                 nos demais casos

onde a unidade tratora é o caminhão ou o caminhão-trator. A justificativa está na seção 8. Aplicada ao Rio Grande do Norte, a regra conta 1.467 caminhões.

## 5. O algoritmo

Para cada ocorrência *i*:

1. Ler a classificação do acidente e escolher a coluna *s* do vetor M, entre sem vítimas, com vítimas e com fatalidade.
2. Contar as pessoas por gravidade, na tabela de pessoas, e multiplicar cada contagem pelo total correspondente da Tabela 1A na coluna *s*.
3. Contar os veículos por classe, na tabela de veículos, e multiplicar cada contagem pelo total correspondente da Tabela 1B na coluna *s*.
4. Somar uma vez o total da Tabela 1C na coluna *s*.
5. Somar as três parcelas. O resultado é o custo em reais de dezembro de 2014.
6. Multiplicar pelo deflator 1,884802. O resultado é o custo em reais de junho de 2026.

O custo de um segmento da malha é a soma dos custos das ocorrências ancoradas nele. A aditividade vale porque o IPEA a assume no método: o custo de um componente não diminui pela multiplicidade dos demais.

## 6. Exemplo trabalhado

A ocorrência 182341, na BR-405 no quilômetro 82,4, em 1º de janeiro de 2019, foi classificada como acidente com vítimas fatais. Ela envolveu três pessoas, sendo dois óbitos e um ileso, e dois veículos, uma motoneta e um automóvel. A coluna aplicada é a de fatalidade.

| Componente | Quantidade | M (dez/2014) | Subtotal (dez/2014) |
|---|---:|---:|---:|
| Morto | 2 | 433.286,69 | 866.573,38 |
| Ileso | 1 | 1.839,94 | 1.839,94 |
| Veículo, classe Motocicletas | 1 | 4.269,83 | 4.269,83 |
| Veículo, classe Automóveis | 1 | 19.323,91 | 19.323,91 |
| Institucional e patrimonial | 1 | 653,06 | 653,06 |
| **Total em dezembro de 2014** | | | **892.660,12** |
| **Total em junho de 2026** (× 1,884802) | | | **1.682.487,58** |

A motoneta entra na classe Motocicletas, conforme o mapeamento, e por isso é valorada em R$ 4.269,83 e não pelo valor de automóvel.

## 7. As quatro categorias por vítima

O objetivo do trabalho é apresentar o custo em quatro categorias compatíveis com a tabela de pessoas da PRF. A memória sustenta duas leituras, e elas respondem a perguntas diferentes.

A **leitura por vítima** apresenta o custo unitário de cada pessoa, pelos componentes da Tabela 1A. Ela responde quanto custa, em média, uma vítima de cada gravidade. É a leitura nova, que a granularidade do vetor C permite e que a planilha V07 não tinha.

| Categoria | Componentes que a compõem | Custo unitário em acidente com vítimas (jun/2026) |
|---|---|---:|
| Vítima leve | pré-hospitalar, hospitalar, pós-hospitalar e perda de produção | 15.963,22 |
| Vítima grave | os mesmos, mais remoção | 235.852,64 |
| Óbito | os mesmos, com perda de produção sobre a sobrevida | 631.733,23 |

A **leitura por ocorrência** distribui o custo total, inclusive veículos e institucional, entre quatro classes, pela vítima mais grave do evento. Ela responde quanto custa um acidente de cada tipo, e é a leitura comparável com a Tabela 3 do TD 2565 e com a planilha V07.

| Categoria da ocorrência | Componentes | Ocorrências no RN |
|---|---|---:|
| Sem vítimas, apenas dano material | veículos e institucional | 1.561 |
| Com vítima leve como mais grave | os anteriores, mais os componentes de saúde e produção dos leves | parcela de 7.820 |
| Com vítima grave como mais grave | os anteriores, com os valores de ferido grave | parcela de 7.820 |
| Com óbito | os anteriores, com os valores de morto | 648 |

Uma ressalva de método precisa acompanhar a categoria dos graves e dos óbitos. A descrição corrente fala em custos previdenciários, e o IPEA calcula o gasto previdenciário, mas o exclui da função de custo, com a justificativa expressa de que somá-lo à perda de produção implicaria dupla contagem. O benefício do INSS financia a perda de renda; o custo social é a perda de produção em si. A categoria, portanto, opera com a perda de produção, e o gasto previdenciário observado entra ao lado, como decomposição de quem paga.

## 8. As três decisões de parâmetro

**A base monetária é junho de 2026**, com o deflator 1,884802 aplicado ao final do cálculo, sobre o total em dezembro de 2014. A escolha preserva a comparabilidade com a planilha V07.

**As pessoas com gravidade não informada entram com custo zero e total declarado à parte.** São 1.703 no Rio Grande do Norte, 7,2% das pessoas. A alternativa de imputar a gravidade pela distribuição observada da própria unidade da federação fica registrada como análise de sensibilidade, e não como cálculo principal. A leitura transparente é preferível à leitura completa e não verificável.

**O mapeamento de veículos segue a tabela da seção 4**, com a regra de composição que os dados impuseram. Três apoios sustentam a regra.

O primeiro é o que o IPEA amostrou. A decomposição de 2006 tem sete classes de veículo, e nenhuma delas é reboque. Se a carreta fosse unidade amostral, apareceria entre os quarenta componentes elementares. O que a pesquisa de campo levantou foi o custo médio de reparo de um caminhão, e caminhão ali significa a composição que trafega.

O segundo é que os dois registros medem coisas diferentes. A PRF conta por identificador de veículo, que é unidade de licenciamento, e o semirreboque tem placa própria. O modelo de custo precisa da unidade econômica de reparo, que é a composição. Aplicar a granularidade administrativa sobre um vetor calibrado na granularidade econômica é o que gera a dupla contagem.

O terceiro é o dado. Das 477 ocorrências com carreta no Rio Grande do Norte, 420 têm a unidade tratora na mesma ocorrência, ou 88%.

A regra adotada trata ainda duas situações que o descarte simples da carreta resolveria mal. Em 57 ocorrências há carreta e nenhuma tratora, e descartar apagaria o caminhão de acidentes que envolveram 66 automóveis e 44 motocicletas; por isso a carreta órfã vale um caminhão. Em 91 ocorrências há mais carretas que tratoras, que são bitrens e rodotrens, uma composição com duas carretas; por isso a contagem segue o número de tratoras, e não o de carretas.

As quatro alternativas foram medidas sobre o Rio Grande do Norte, na classe Caminhões, a preços de junho de 2026.

| Regra | Unidades | Custo da classe |
|---|---:|---:|
| Carreta nunca conta | 1.410 | 140.079.515,34 |
| **Composição uma vez; carreta órfã vale um caminhão** | **1.467** | **146.114.628,54** |
| Toda carreta excedente conta | 1.573 | 156.421.385,45 |
| Tratora e carreta contam separadamente | 2.024 | 200.556.347,82 |

A regra adotada recupera R$ 6,0 milhões que o descarte simples perderia e evita R$ 54,4 milhões de dupla contagem.

## 9. Verificação prevista

O cálculo será conferido em três frentes. A soma por classe de ocorrência deve reproduzir a ordem de grandeza da Tabela 3 do TD 2565, quando aplicada à base nacional. O total do Rio Grande do Norte deve ficar próximo dos R$ 2,30 bilhões registrados na planilha V07, cuja contagem de ocorrências diverge da base reconstruída em 0,3%. E o deflator deve reproduzir os três custos por acidente da aba de parâmetros da V07, o que já se confirmou para o acidente sem vítimas.
