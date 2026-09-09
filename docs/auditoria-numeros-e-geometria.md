**Universidade Federal do Rio Grande do Norte**
**Instituto Metrópole Digital**
**Programa de Pós-Graduação em Tecnologia da Informação**
**Disciplina:** Tópicos Avançados em Engenharia de Software 2 (Desenv. de Software com IA)
**Professor:** Jean Mário Moreira de Lima
**Alunos:** Flávio Eduardo Batista Moreira e Bruno dos Santos Fernandes da Silva

# Auditoria dos números e da geometria do mapa

## Conferência do piloto do Rio Grande do Norte, a preços de junho de 2026

---

## 1. O que este documento audita

O mapa dos trechos críticos passou a exibir uma tabela de segmentos, o custo por
categoria e o traçado de cada trecho. Cada um desses números foi conferido contra o
banco consolidado antes de entrar na apresentação. Este documento registra as
conferências, os erros encontrados no caminho e as correções, para que a banca
acompanhe a origem de cada valor.

## 2. A tabela dos 171 segmentos reproduz o banco

A tela lista 171 segmentos com ocorrência ancorada. A consulta que alimenta a tabela
foi reexecutada contra o banco e comparada linha a linha com o que a tela mostra. Os
cinquenta primeiros segmentos conferem em todas as colunas: número de ocorrências,
custo social, volume médio diário anual, custo por quilômetro e custo por
veículo-quilômetro. Não houve divergência.

A aritmética do agregado também fecha. A soma das ocorrências dos 171 segmentos dá
10.008. O banco tem 10.029 ocorrências no estado, e as 21 restantes são as que não
ancoraram em nenhum segmento. A soma do custo por segmento é R$ 1.913.595.818, e essas
21 ocorrências completam o total de R$ 1.915.035.912 do estado.

## 3. O custo por categoria diverge do IPEA na direção prevista

As quatro categorias, compatíveis com a tabela de pessoas da Polícia Rodoviária
Federal, distribuem o custo do estado assim:

| Categoria | Ocorrências | Custo | Médio por ocorrência |
|---|---:|---:|---:|
| sem vítimas | 1.561 | R$ 58,5 mi | R$ 37.481 |
| com vítima leve | 5.410 | R$ 378,8 mi | R$ 70.025 |
| com vítima grave | 2.410 | R$ 795,1 mi | R$ 329.927 |
| com óbito | 648 | R$ 682,6 mi | R$ 1.053.351 |
| total | 10.029 | R$ 1.915,0 mi | |

O IPEA agrega as lesões numa classe só, com feridos. Reunindo as vítimas leves e
graves para comparar, o custo médio calculado por componente fica cerca de 16% abaixo
da média por acidente da Tabela 3 do Texto para Discussão 2565, a preços de junho de
2026:

| Classe do IPEA | Cálculo por componente | Tabela 3 do IPEA | Desvio |
|---|---:|---:|---:|
| sem vítimas | R$ 37.481 | R$ 44.291 | −15,4% |
| com feridos | R$ 150.122 | R$ 182.350 | −17,7% |
| com fatal | R$ 1.053.351 | R$ 1.253.057 | −15,9% |

O desvio tem o sinal e a causa já registrados no documento de achados. A média do
IPEA carrega a composição de vítimas e de veículos do Brasil de 2014. O Rio Grande do
Norte tem mais motocicletas, que são o veículo de menor custo, e 1,10 morte por
acidente fatal contra 1,22 do país em 2014. O cálculo por componente, feito com a
composição real do estado, produz um custo por acidente menor, e a média nacional
superestima o custo local.

A triangulação com a planilha V07 confirma a coerência. A V07 aplica ao mesmo estado a
média agregada do IPEA e chega a R$ 2,302 bilhões. O cálculo por componente chega a
R$ 1,915 bilhão, 16,8% abaixo, o mesmo desvio que aparece por categoria. As contagens
das duas fontes também se aproximam: a V07 registra 1.547 sem vítimas, 7.803 com
feridos e 647 fatais; a reconstrução registra 1.561, 7.820 e 648, dentro dos 0,3% de
diferença de contagem já documentados.

## 4. Uma correção de valor de referência do IPEA

A primeira versão desta conferência usou, para as classes com feridos e com fatal, os
valores de R$ 91.531,44 e R$ 646.762,94 a preços de dezembro de 2014, recuperados de
memória. A leitura da aba de parâmetros da planilha V07, que cita o Texto para
Discussão 2565 como fonte, mostrou que os valores corretos são R$ 96.747,79 e
R$ 664.821,46. A tabela da seção anterior já usa os valores conferidos na planilha. O
valor da classe sem vítimas, R$ 23.498,77, já estava correto e é o que o deflator de
1,884802 leva a R$ 44.290,53.

## 5. O custo por quilômetro do trecho mais curto

O segmento 101BRN0085 apareceu com R$ 27.694.637 por quilômetro, o maior da tabela, e
o valor levantou dúvida. A conferência mostra que ele está correto, e que a estranheza
vem da extensão. O trecho tem 0,9 quilômetro e acumulou R$ 24.925.173 em 175 sinistros
de 2019 a 2025. A divisão pela extensão curta eleva o número: R$ 24.925.173 dividido
por 0,9 dá R$ 27.694.637 por quilômetro.

Dois fatos explicam a magnitude. O valor cobre sete anos, e não um; por ano, cai para
R$ 3.956.377 por quilômetro. E o trecho é o mais curto entre os carregados, um segmento
da BR-101 dentro da região metropolitana de Natal, com o maior fluxo do estado, 58.617
veículos por dia, e 175 sinistros comprimidos em menos de um quilômetro. Um custo
parecido espalhado por um trecho longo dá custo por quilômetro baixo: o 110BRN0022, com
quase o dobro do custo distribuído em 36,1 quilômetros, dá R$ 1,16 milhão por
quilômetro.

A leitura por exposição corrige a distorção. Normalizado pelo volume, o 101BRN0085 tem
custo por veículo-quilômetro de 1,2944, valor baixo, porque o risco por veículo que
passa é pequeno onde o tráfego é intenso. O trecho vazio é o que sobe nessa leitura, o
110BRN0025, com volume de 3.184 veículos por dia e custo por veículo-quilômetro de
11,35.

## 6. As colunas anuais

A pedido, a tabela ganhou as colunas de custo por quilômetro por ano e de custo por
veículo-quilômetro por ano, ao lado das acumuladas. Elas dividem o valor pelo período
observado, contado do primeiro ao último ano com ocorrência na unidade da federação. No
Rio Grande do Norte, o período é de 2019 a 2025, sete anos, apurado do próprio banco, e
não fixado no código, de modo que a conta se estende a outras unidades e a anos futuros
sem alteração.

## 7. A geometria por sinistros foi descartada por medição

A primeira versão do desenho traçou cada trecho ligando os seus sinistros em ordem de
quilômetro, por falta de geometria da via no banco. O resultado poluiu o mapa: com os
sinistros esparsos e fora de ordem espacial, as linhas cruzaram o estado e não
representaram o traçado das rodovias. A aproximação foi mantida apenas como recuo, para
os poucos trechos sem geometria oficial.

A correção veio da base geométrica do DNIT, no formato shapefile, disponível no
repositório privado. A base traz uma polilinha por trecho, no campo `vl_codigo`,
idêntico ao código do nosso banco. Na safra 202507A, 169 dos 171 segmentos do estado
casaram pelo código, ou 98,8%. Os dois restantes, 101BRN0130 e 226BRN0176, foram
recodificados entre safras e permanecem com a aproximação, agora desenhada em linha
tracejada, para não se confundir com a via oficial.

O traçado passou por simplificação de Douglas-Peucker com tolerância de cerca de 90
metros, abaixo do que se distingue na escala do estado. Os 97.002 pontos brutos caíram
para 905, uma redução de 99%, e o conjunto ocupa 48 quilobytes. A geometria foi gravada
numa tabela do banco consolidado, `geometria_segmento`, com o código, a safra e a lista
de pontos, e o banco cresceu de 8,88 para 8,96 megabytes. A base bruta, de 88 megabytes,
permanece fora do controle de versão.

A caixa flutuante que aparece ao passar o mouse sobre um trecho mostra os mesmos dez
campos da tabela: segmento, BR, extensão, ocorrências, custo social, volume médio
diário anual, e as quatro leituras de criticidade. O trecho sob o cursor engrossa e
muda de cor, e volta ao estado anterior ao sair.

## 8. Cobertura de testes

A camada de consulta e a de aplicação têm 131 testes automatizados, executados a cada
mudança. Cobrem a agregação por segmento sem multiplicar o custo por safra, as duas
leituras de criticidade, as colunas anuais, a recusa de ordenação fora da lista
permitida, a resposta a banco sem as tabelas de sinistro, a ingestão da geometria a
partir de um shapefile de teste, a simplificação que preserva os pontos extremos, e a
preferência pela geometria oficial com recuo para a aproximação. As três conferências
numéricas deste documento foram executadas contra o banco real, e não sobre dados de
teste.

## 9. Registro das correções da sessão

A sessão acumulou correções que valem registro, no mesmo espírito das anteriores.

A tabela de cores do mapa usava chaves de categoria que não existiam no banco, e por
isso os pontos saíam cinza. As chaves corretas, apuradas no banco, são `sem_vitimas`,
`com_vitima_leve`, `com_vitima_grave` e `com_obito`.

O script da página quebrava porque a legenda usava uma constante declarada depois do
bloco do mapa. Com `const`, o uso antes da declaração interrompe a execução, e nem os
pontos nem a legenda apareciam. A declaração foi movida para antes do bloco.

Os valores de referência do IPEA para as classes com feridos e com fatal foram
corrigidos, como registra a seção 4.

A geometria por sinistros foi substituída pela oficial, como registra a seção 7.

Cada correção seguiu a mesma regra: o número foi conferido contra o banco, ou contra a
fonte primária, antes de ser aceito.
