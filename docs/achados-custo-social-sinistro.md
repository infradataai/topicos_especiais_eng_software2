**Universidade Federal do Rio Grande do Norte**
**Instituto Metrópole Digital**
**Programa de Pós-Graduação em Tecnologia da Informação**
**Disciplina:** Tópicos Avançados em Engenharia de Software 2 (Desenv. de Software com IA)
**Professor:** Jean Mário Moreira de Lima
**Alunos:** Flávio Eduardo Batista Moreira e Bruno dos Santos Fernandes da Silva

# Achados do custo social dos sinistros rodoviários

## Por que a unidade de cálculo é a unidade da federação

---

## 1. O achado em uma frase

A média de custo por acidente publicada pelo IPEA carrega a composição de vítimas e de veículos do Brasil de 2014. Aplicá-la a um estado produz um erro que varia de menos 2,1% a mais 37,7%, conforme o estado. O cálculo por componente, feito com a composição real de cada unidade da federação, elimina esse erro e é o que justifica adotar a unidade da federação como unidade de cálculo, com as cinco regiões e o país como agregações de comparação.

## 2. Como o achado apareceu

O custo social do Rio Grande do Norte foi calculado pelo produto escalar entre o vetor C, que conta as pessoas por gravidade e os veículos por classe de cada ocorrência, e o vetor M de custos médios padrão da Tabela 1 do Texto para Discussão 2565. O resultado, sobre 10.029 ocorrências de 2019 a 2025, foi de R$ 1,915 bilhão a preços de junho de 2026.

A planilha V07, que aplica ao mesmo estado as três médias por acidente da Tabela 3 do mesmo documento, registra R$ 2,302 bilhões. A diferença de 16,8% exigiu investigação antes de qualquer número ser aceito.

## 3. A explicação da divergência

A Tabela 3 do IPEA traz o custo total nacional de 2014 dividido pelo número de acidentes de cada classe. Ela é uma média, e toda média embute a composição da população que a gerou. Duas características do Rio Grande do Norte se afastam da composição nacional de 2014.

A primeira é a letalidade por evento. O Brasil de 2014 registrou 8.233 mortes em 6.743 acidentes fatais, ou 1,22 morte por acidente. O Rio Grande do Norte registra 713 mortes em 648 acidentes fatais, ou 1,10. São 10% menos vítimas fatais por evento fatal, e o componente de perda de produção do morto, que responde pela maior parcela do custo, entra proporcionalmente menos vezes.

A segunda é a frota envolvida. No Rio Grande do Norte, 35,5% dos veículos envolvidos em sinistros são motocicletas, motonetas ou ciclomotores. No vetor M, a motocicleta em acidente fatal custa R$ 4.269,83 e o automóvel custa R$ 19.323,91, uma razão de 4,5 vezes. Um estado de frota motociclística tem custo de veículo estruturalmente menor.

A conclusão é que a divergência mede o que se propunha a medir. A V07 aplica o Brasil de 2014 ao Rio Grande do Norte; o produto escalar mede o Rio Grande do Norte. E ela revela um viés que a planilha carregava sem saber: aplicar a média nacional a um estado de frota mais motociclística superestima o custo dos veículos.

## 4. A composição varia entre os estados

Se a composição fosse homogênea no país, o achado seria uma curiosidade local. A medição sobre a base deduplicada da PRF, de 2019 a 2025, mostra o contrário.

| Característica | Mínimo | Máximo | Razão |
|---|---|---|---|
| Motocicletas na frota envolvida | 14,8% (MT e AM) | 37,7% (AC) | 2,55 vezes |
| Óbitos por acidente fatal | 1,079 (SP) | 1,250 (AP) | 1,16 vez |
| Veículos por ocorrência | 1,77 (AC) | 2,40 (MT) | 1,36 vez |

A participação da motocicleta varia por um fator de dois e meio entre os extremos, e segue um padrão regional: os estados do Norte e do Nordeste concentram as maiores participações, e os do Centro-Oeste e do Sul as menores. Nenhuma média nacional descreve bem os dois grupos ao mesmo tempo.

## 5. O viés medido nas 27 unidades da federação

O cálculo por componente foi executado sobre as 473.646 ocorrências do país, de 2019 a 2025, e comparado com o que a média nacional produziria sobre as mesmas ocorrências. O viés positivo significa que a média nacional superestima o custo daquele estado.

| Unidade da federação | Ocorrências | Cálculo por componente (R$ bi) | Média nacional (R$ bi) | Viés |
|---|---:|---:|---:|---:|
| DF | 7.080 | 1,01 | 1,40 | +37,7% |
| SP | 31.421 | 4,96 | 6,56 | +32,2% |
| RJ | 36.512 | 6,08 | 8,00 | +31,5% |
| RN | 10.029 | 1,92 | 2,31 | +20,5% |
| SC | 55.499 | 9,78 | 11,44 | +17,0% |
| PB | 11.344 | 2,28 | 2,65 | +16,3% |
| RS | 33.278 | 6,12 | 7,07 | +15,6% |
| AC | 1.834 | 0,38 | 0,43 | +15,2% |
| RO | 10.153 | 1,97 | 2,20 | +11,5% |
| PR | 51.951 | 10,62 | 11,73 | +10,5% |
| RR | 1.404 | 0,36 | 0,40 | +10,4% |
| SE | 3.931 | 0,86 | 0,94 | +9,3% |
| CE | 10.346 | 2,54 | 2,77 | +8,9% |
| PE | 19.849 | 4,76 | 5,18 | +8,9% |
| AP | 1.105 | 0,23 | 0,25 | +7,8% |
| GO | 22.521 | 4,95 | 5,31 | +7,3% |
| ES | 17.463 | 3,72 | 3,95 | +6,0% |
| PI | 9.087 | 2,32 | 2,45 | +6,0% |
| MS | 11.439 | 2,60 | 2,74 | +5,2% |
| MG | 61.597 | 13,98 | 14,59 | +4,4% |
| AL | 4.394 | 1,21 | 1,25 | +3,7% |
| AM | 856 | 0,23 | 0,23 | +2,9% |
| PA | 6.441 | 2,15 | 2,18 | +1,3% |
| MT | 16.154 | 3,95 | 3,96 | +0,3% |
| BA | 25.725 | 7,38 | 7,39 | +0,2% |
| TO | 4.224 | 1,25 | 1,23 | −1,8% |
| MA | 8.009 | 2,83 | 2,77 | −2,1% |
| **Brasil** | **473.646** | **100,44** | **111,39** | **+10,9%** |

O intervalo tem 39,8 pontos percentuais, e o sinal se inverte entre os extremos. No Distrito Federal, em São Paulo e no Rio de Janeiro a média nacional superestima o custo em cerca de um terço. No Maranhão e no Tocantins ela subestima. Um erro que muda de sinal conforme o estado não se corrige por fator único, e é por isso que a agregação precisa ser construída de baixo para cima.

O viés agregado do país, de 10,9%, tem causa própria: a composição de 2019 a 2025 difere da de 2014, com mais motocicletas e menos vítimas fatais por evento. A média de 2014 já não descreve bem nem o Brasil atual.

## 6. Custo social por região

As cinco regiões saem da soma das unidades da federação, e não de um cálculo próprio. Elas servem à comparação, e não à estimativa.

| Região | Ocorrências | Custo por componente (R$ bi) | Média nacional (R$ bi) | Viés | Custo médio por ocorrência |
|---|---:|---:|---:|---:|---:|
| Sudeste | 146.993 | 28,74 | 33,09 | +15,1% | 195.543 |
| Sul | 140.728 | 26,51 | 30,24 | +14,1% | 188.411 |
| Nordeste | 102.714 | 26,08 | 27,71 | +6,3% | 253.942 |
| Centro-Oeste | 57.194 | 12,52 | 13,41 | +7,1% | 218.832 |
| Norte | 26.017 | 6,58 | 6,93 | +5,4% | 252.840 |
| **Brasil** | **473.646** | **100,44** | **111,39** | **+10,9%** | **212.048** |

O custo médio por ocorrência do Nordeste supera o do Sul em 35%, apesar de o Sul concentrar mais ocorrências. A leitura por região confirma o padrão da seção 4: onde a frota é mais motociclística e a letalidade por evento é maior, o custo médio por ocorrência sobe.

## 7. Resultado nacional por categoria

| Categoria da ocorrência | Ocorrências | Custo (R$ bi) | Custo médio |
|---|---:|---:|---:|
| Com óbito | 33.729 | 38,88 | 1.152.858 |
| Com vítima grave | 98.849 | 35,50 | 359.166 |
| Com vítima leve | 260.727 | 22,99 | 88.187 |
| Sem vítimas | 80.341 | 3,05 | 38.022 |

O total de R$ 100,44 bilhões cobre sete anos nas rodovias federais, o que dá R$ 14,35 bilhões por ano. As ocorrências com óbito são 7,1% do total e respondem por 38,7% do custo.

## 8. A decisão que o achado sustenta

A unidade de cálculo passa a ser a unidade da federação. As cinco regiões e o país são agregações das unidades, calculadas por soma, e entram como termo de comparação. Nenhum resultado estadual é obtido por rateio de um total nacional.

A mesma lógica se estende à comparação entre os regimes de administração da malha, o trecho não concedido sob o DNIT e o trecho concedido sob a ANTT. A comparação entre regimes exige que cada ocorrência seja valorada pela sua própria composição antes de ser atribuída ao regime, sob pena de a diferença observada entre regimes refletir a composição da frota e não a administração da via. Essa etapa depende da ancoragem no segmento do SNV, com a marcação de concessão, e está prevista para a fase seguinte.

## 9. A comparação entre regimes não cabe no piloto

A ancoragem das ocorrências do Rio Grande do Norte nos segmentos do SNV revelou um limite que muda o desenho do trabalho. Na malha do estado há 208 segmentos de jurisdição federal, todos sob administração do DNIT, e 206 estaduais e municipais coincidentes. Não há um único segmento de concessão federal.

A comparação entre o trecho administrado pelo DNIT e o concedido à ANTT, portanto, não existe dentro do Rio Grande do Norte. Ela só se realiza na escala nacional, onde a safra de janeiro de 2025 registra 1.111 segmentos concedidos contra 4.801 federais.

O achado reforça a divisão já adotada. O piloto do estado demonstra o método, valora o custo por segmento e produz o mapa de trechos críticos. A comparação entre regimes pertence ao trabalho nacional, e tentá-la no piloto produziria uma tabela com uma única linha preenchida.

A ancoragem também se validou contra fonte externa. Das 10.029 ocorrências, 10.008 foram ancoradas, ou 99,8%, e a malha coberta soma 1.666,5 km, a 1,1% dos 1.648,7 km que a planilha V07 registra para o estado.

## 10. A mesma fonte muda de formato entre safras

Dois defeitos de leitura apareceram no trabalho, em fontes diferentes, e são o mesmo defeito.

O arquivo de sinistros da PRF de 2022 traz a data em `DD/MM/AAAA`, enquanto os outros seis anos usam `AAAA-MM-DD`. Sob inferência automática de formato, as datas cujo dia passa de 12 viram nulo e as demais têm dia e mês trocados. A perda medida foi de 791 das 1.288 ocorrências daquele ano.

A planilha do SNV de novembro de 2025 grava a quilometragem com vírgula decimal, enquanto as safras anteriores usam ponto. A conversão numérica devolveu nulo para a safra inteira, e nenhuma ocorrência de 2025 chegou a ancorar. A taxa de ancoragem ficou em 83,4% até o defeito ser encontrado, e subiu para 99,8% depois da correção.

Os agregados do DATASUS trazem marca de ordem de byte no início do cabeçalho, o que faz a primeira coluna ser lida com um caractere invisível no nome, e nenhuma consulta por nome funciona.

Os arquivos do VMDa de 2017 e de 2021 usam nomes de coluna diferentes dos demais anos, e a aba de dados muda de nome a cada edição, de `SNV_201903A` a `VMDa 2021` e `VMDa2025_SNV202401A`.

São quatro casos, em três órgãos, quatro formatos de arquivo e períodos distintos, exibindo a mesma falha estrutural: a fonte muda a convenção entre versões, sem aviso, e a leitura por inferência aceita a mudança em silêncio. O prejuízo não é o erro visível, e sim o dado que desaparece sem mensagem.

A conclusão de método é que o reconhecimento de formato precisa ser declarado e verificado, e não inferido. Cada formato aceito é reconhecido pelo seu próprio padrão, e o que não casa vira nulo declarado, contabilizado por um validador. É o princípio que o ADR-009 fixou, e estes dois casos são a sua evidência empírica.

Um terceiro defeito, de natureza diferente, vale registro pelo tamanho do efeito. A consulta que agrega o custo por segmento juntava a ancoragem à tabela de segmentos apenas pelo código, sem a safra. Como o mesmo código existe em todas as safras, cada ocorrência casava com sete linhas, e o custo do estado saltava para R$ 11 bilhões contra os R$ 1,9 bilhão reais. O defeito só apareceu porque o total agregado foi conferido contra o total calculado, o que sustenta manter as duas contas em pontos separados do sistema.

## 11. O trecho caro e o trecho perigoso não são o mesmo

A pergunta que motivou a criticidade por exposição tinha uma resposta em aberto: um trecho de custo alto é perigoso, ou apenas movimentado? Com o volume médio diário anual do Plano Nacional de Contagem de Tráfego carregado, a resposta foi medida.

Os oito primeiros trechos de cada leitura coincidem em apenas dois. Seis dos oito aparecem numa lista e não na outra.

O ranque por custo por quilômetro é dominado pela BR-101, com volume mediano de 49.526 veículos por dia. O ranque por custo por veículo-quilômetro é dominado pelas BR-110, BR-304 e BR-405, com volume mediano de 2.934 veículos por dia. A diferença de densidade de tráfego entre os dois grupos é de dezessete vezes.

| Leitura | Segmento | BR | VMDa | Custo por km (R$) | Custo por veículo-km (R$) |
|---|---|---:|---:|---:|---:|
| Por quilômetro | 101BRN0085 | 101 | 58.617 | 27.694.637 | 1,294 |
| Por quilômetro | 101BRN0080 | 101 | 58.617 | 19.972.912 | 0,934 |
| Por quilômetro | 101BRN0110 | 101 | 40.435 | 18.259.691 | 1,237 |
| Por exposição | 110BRN0025 | 110 | 3.184 | 13.188.315 | 11,348 |
| Por exposição | 304BRN0095 | 304 | 1.268 | 4.321.703 | 9,338 |
| Por exposição | 405BRN0010 | 405 | 2.234 | 7.310.283 | 8,965 |

O segmento 304BRN0095 ilustra o ponto. Ele custa R$ 4,3 milhões por quilômetro, quase seis vezes menos que o primeiro colocado da BR-101, e é sete vezes mais caro por veículo que nele trafega.

A inversão se repete na leitura por rodovia. A BR-101 lidera o custo por quilômetro, com R$ 3,42 milhões, e cai para o quinto lugar no custo por exposição, com R$ 0,671. A BR-110 é a última em custo absoluto e a primeira em risco por exposição, com R$ 1,755.

A consequência para a política pública é direta. Um plano de intervenção guiado apenas pelo custo absoluto concentraria recursos na BR-101, onde o custo se explica em boa parte pelo volume de tráfego. A leitura por exposição aponta trechos de menor movimento em que cada veículo corre mais risco, e que a leitura por custo não revelaria.

A exposição foi medida em 89% dos segmentos com ocorrência. Os 11% restantes permanecem no ranque por quilômetro, com a exposição declarada como ausente, e não imputada.

## 12. Limites do achado

A comparação desta análise é entre dois métodos aplicados à mesma base, e não entre o resultado atual e o resultado publicado pelo IPEA em 2014. As duas bases têm anos diferentes, e a diferença de composição entre 2014 e o período de 2019 a 2025 faz parte do que se mede.

Os custos unitários do vetor M continuam sendo os da pesquisa amostral de 2005 e 2006, corrigidos por IPCA. O achado corrige a aplicação da média, e não a idade dos custos unitários. A substituição de componentes por valores observados no SIH, no SAMU e no INSS segue prevista, e é o próximo ganho de precisão.

As pessoas sem gravidade informada entram com custo zero, o que faz de todo resultado um piso. São 7,2% das pessoas no Rio Grande do Norte.

## 12. Procedência

O cálculo está implementado em `custo_social_core/custo.py`, com os parâmetros em `custo_social_core/vetor_m.py`, sob a spec de `openspec/changes/calculo-custo/` e as decisões do ADR-011. A ingestão está em `custo_social_core/ingestao_prf.py`, sob o ADR-009. A ancoragem e a consolidação estão em `custo_social_core/snv.py` e `custo_social_core/persistencia.py`, sob a spec de `openspec/changes/consolidacao-e-snv/`.

A memória de cálculo, com as três subtabelas do vetor M e o exemplo trabalhado, está em `docs/memoria-calculo-CM.md`. Os três defeitos relatados na seção 10 estão travados por testes de regressão, que quebram se qualquer um deles voltar.

Os resultados por ocorrência, por unidade da federação, por região e por segmento estão no banco consolidado, na camada de dados, fora do controle de versão. O banco é artefato derivado e se regenera com `python -m scripts.consolidar_e_ancorar --uf RN --snv <pasta das planilhas>`.
