**Universidade Federal do Rio Grande do Norte**
**Instituto Metrópole Digital**
**Programa de Pós-Graduação em Tecnologia da Informação**
**Disciplina:** Tópicos Avançados em Engenharia de Software 2 (Desenv. de Software com IA)
**Professor:** Jean Mário Moreira de Lima
**Aluno:** Flávio Eduardo Batista Moreira

# Escopo do Projeto Final

## Piloto RN de custo social de sinistros rodoviários e caminho de escala nacional

---

## 1. Objetivo e enquadramento

O projeto final aplica os três módulos da disciplina a um caso real da tese de doutorado do aluno: a valoração e a espacialização do custo social dos sinistros nas rodovias federais. O entregável da disciplina é um piloto restrito ao Rio Grande do Norte, que calcula o custo social por segmento da rodovia e projeta em mapa os trechos críticos. O mesmo código, parametrizado por unidade da federação, é o que depois escala para o Brasil, na continuidade da tese.

A escolha do RN como piloto atende a dois objetivos ao mesmo tempo. Entrega um trabalho fechado e apresentável no prazo da disciplina, e produz a primeira instância verificável do pipeline nacional que a tese precisa. O piloto é o Brasil rodado com um filtro de estado, e por isso alimenta a tese na mesma medida em que fecha a disciplina.

## 2. Ponto de partida

O trabalho não começa do zero. A planilha `Custo_Social_Parametros_e_Resultados_V07.xlsx` já traz o custo por unidade da federação com a extensão de malha vinda do SNV, a correção de subregistro entre o SIM e a PRF, a completude do registro de ferido grave triangulada entre SIH, RENAEST e PRF, o dano material da PRF por classe de montante e um cenário de custo por vida. Para o RN, a planilha já registra 1.547 sinistros sem vítimas, 7.803 com feridos e 647 fatais no período, sobre 1.648,7 km de malha, com custo social de R$ 2,30 bilhões e valor médio de R$ 230 mil por sinistro.

As quatro bases de dados que sustentam o piloto estão coletadas e no mesmo referenciamento linear. Os sinistros da PRF trazem BR, quilômetro, latitude, longitude e a contagem de ilesos, feridos leves, feridos graves e mortos por pessoa. O SNV traz a definição do segmento por safra, de 2018 a 2025. O PNCT/VMDa traz o volume médio diário anual por unidade de tráfego, de 2017 a 2025, cada safra amarrada à safra correspondente do SNV. Os pedidos da LAI trazem os componentes observados do custo: o INSS para a perda de produção, o SAMU para o atendimento pré-hospitalar, o SIH e o SIM do DATASUS para a saúde e a mortalidade, e a PRF para o dano material.

## 3. Modelo de custo em quatro categorias

A refinação parte de uma decisão de método. O custo do Ipea, no Texto para Discussão 2565, é definido por ocorrência e em três classes: sem vítimas, com vítimas feridas e com vítima fatal. As quatro categorias pretendidas para o piloto misturam dois níveis de análise. O sinistro sem feridos, com dano material apenas, é uma categoria por ocorrência. O ferido leve, o ferido grave e o óbito são categorias por vítima, e a base da PRF sustenta esse nível de vítima nas colunas de contagem por pessoa.

A abordagem adotada é híbrida. O custo do Ipea por ocorrência permanece como âncora de referência e validação, por ser a estimativa oficial, comparável e defensável na banca. A refinação usa os dados da LAI para decompor a classe com vítimas feridas em leves e graves. A razão de custo entre as duas sai do observado: o SIH informa o custo de internação do ferido grave, o INSS informa a perda de produção por incapacidade, e a PRF informa a proporção entre leves e graves por ocorrência. O resultado é um custo por vítima e por gravidade, ancorado em desembolso público observável, que triangula contra o total do Ipea em vez de somar sobre ele.

A triangulação evita a dupla contagem, que é o risco maior do refino e que o documento `Fontes_Custo_Social_Sinistros.docx` já nomeia. O valor do Ipea embute a saúde, a perda de produção e o dano a veículos. Somar de novo os componentes observados da LAI sobre esse valor contaria o mesmo custo duas vezes. Por isso os componentes da LAI entram como decomposição e como auditoria do valor do Ipea, sem se somar a ele. As abas `Fonte_triangulacao_uf_ano`, `Completude_FeridoGrave` e `Correcao_Subregistro` da planilha são as três pernas dessa triangulação.

A atualização para valores correntes deixa de depender só do deflator. Hoje o custo é o valor do Ipea de dezembro de 2014 corrigido pelo IPCA até junho de 2026. O refino substitui parte dessa correção por valores observados recentes, porque o benefício do INSS é nominal por ano, a autorização de internação hospitalar do SIH é nominal e o atendimento do SAMU é por evento. O número resultante fica mais próximo do desembolso real.

## 4. Espacialização no SNV e trechos críticos

A espacialização é o núcleo do pipeline e o que amarra o projeto à disciplina. Cada sinistro é ancorado ao segmento do SNV pelo referenciamento linear, com a chave de BR, unidade da federação e quilômetro. Os sinistros e o custo social são agregados por segmento, e os segmentos são ranqueados para a leitura de trecho crítico.

Dois cuidados que os dados impõem entram como regra. A safra do SNV do ano do sinistro tem de casar com a malha vigente naquele ano, porque o traçado e a quilometragem mudam entre safras, e ancorar um sinistro de 2019 na malha de 2025 desloca o ponto. A leitura de trecho crítico por custo absoluto tende a apontar apenas as rodovias movimentadas, o que o item seguinte corrige.

## 5. Criticidade ajustada por exposição

Um trecho com custo alto pode ser apenas um trecho de tráfego intenso, e não um trecho perigoso. Dividir o custo social do segmento pela exposição de tráfego separa o corredor caro do corredor de fato letal. O denominador vem do PNCT/VMDa, com o volume médio diário anual por unidade, no mesmo referenciamento do SNV, o que dispensa qualquer cruzamento aproximado.

A medida se alinha ao tratamento de exposição que a tese já emprega como *offset* e torna a classificação de trecho crítico defensável na banca. O piloto apresenta o mapa do RN em duas leituras lado a lado, o custo absoluto por quilômetro e o custo por exposição. A diferença entre as duas leituras é, ela mesma, um achado do trabalho, porque revela onde o custo se concentra por volume e onde se concentra por risco.

## 6. Correção de subregistro no mapa

A PRF registra menos óbitos que o SIM em parte da malha, e um mapa que ignore isso subestima o custo onde o registro falha. Por isso cada segmento aparece em dois valores: o observado pela PRF e o corrigido pelo fator da aba `Correcao_Subregistro`, que reclassifica a série entre os cenários de piso, central e teto. A leitura corrigida impede que a ausência de registro seja lida como ausência de custo.

## 7. Arquitetura e reuso entre o RN e o Brasil

A arquitetura segue a decisão do ADR-003, o monólito modular, aplicada ao dado. Toda função de cálculo é escrita parametrizada pela unidade da federação, sem o RN embutido no código. O piloto RN é o pipeline nacional com o filtro na sigla do estado, sobre o mesmo esquema, o mesmo referenciamento linear e o mesmo modelo de custo. O que é próprio do RN fica isolado numa camada fina de configuração: a extensão do mapa, os corredores locais das BR-101, BR-304, BR-226 e BR-406, e a validação cruzada com o SIM do estado. Aprofundar no RN é descer ao nível de segmento e de corredor com lógica genérica, de modo que a escala para o Brasil amplie o filtro sem reescrever o núcleo.

## 8. Topologia de repositórios

O piloto RN entra como uma pasta de projeto final no repositório público da disciplina, `topicos_especiais_eng_software2`, onde as três atividades assíncronas já estão e onde o professor acompanha o histórico. Ele carrega o núcleo parametrizado, rodado para o RN, os dados do estado, os mapas, o relatório, os ADRs e os slides. A visibilidade pública é possível porque toda a entrada é dado aberto, e as respostas da LAI usadas não têm dado pessoal.

O escalonamento nacional entra num repositório privado novo, `custo-social-sinistro-BR`, restrito ao aluno, ao coautor e aos dois professores. O resguardo protege o resultado nacional ainda não publicado e a colaboração da tese, já que o código é o mesmo do piloto. O repositório privado consome o núcleo escrito uma vez e guarda os dados de todas as unidades da federação e a análise nacional. Essa divisão preserva o princípio de escala por parâmetro, porque o privado reusa o núcleo do público em vez de manter uma cópia que divergiria. A decisão fica registrada em ADR próprio. Qualquer arquivo com dado pessoal, como o microdado do SIM, permanece fora do controle de versão nos dois repositórios.

## 9. Plano por fases

A primeira fase entrega o modelo de custo em quatro categorias, com a decomposição da classe de feridos e a triangulação contra o Ipea, sobre os dados do RN. A segunda fase entrega a espacialização, com o referenciamento linear dos sinistros do RN nos segmentos do SNV por safra casada. A terceira fase entrega o mapa dos trechos críticos, nas duas leituras de custo por quilômetro e custo por exposição, com a camada de subregistro. A quarta fase entrega o relatório e a apresentação, no formato das atividades anteriores.

O caminho de escala nacional fica documentado como continuidade, com o núcleo já parametrizado e o repositório privado preparado para receber as demais unidades da federação. A escala fica fora da entrega da disciplina e permanece como o desenho que garante o reuso do piloto na tese, sem refação.

## 10. Riscos e limites

A decomposição do custo depende da completude dos registros de gravidade, que varia entre as unidades da federação, e por isso o piloto assume a triangulação com o SIH e o RENAEST em vez de confiar num registro único. A exposição do PNCT/VMDa cobre a rede federal amostrada, e os segmentos sem posto de contagem recebem a exposição por imputação declarada no método. A safra do SNV precisa casar com o ano do sinistro, e o pipeline trata o descasamento de safra como erro que interrompe o cálculo. As respostas de pavimento e de exposição ainda pendentes na LAI entram como caso previsto, sem quebrar o cálculo que já roda.
