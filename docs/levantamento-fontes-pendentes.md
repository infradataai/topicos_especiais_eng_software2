**Universidade Federal do Rio Grande do Norte**
**Instituto Metrópole Digital**
**Programa de Pós-Graduação em Tecnologia da Informação**
**Disciplina:** Tópicos Avançados em Engenharia de Software 2 (Desenv. de Software com IA)
**Professor:** Jean Mário Moreira de Lima
**Alunos:** Flávio Eduardo Batista Moreira e Bruno dos Santos Fernandes da Silva

# Levantamento das fontes ainda não ingeridas

## O que sobra na pasta de dados, quanto custa e quanto rende

---

## 1. O ponto de partida

O banco consolidado reúne quatro fontes: os sinistros da PRF, os segmentos do SNV, o volume de tráfego do PNCT e dois agregados do DATASUS. Da pasta de dados do projeto, com 965 arquivos e 35 GB, entraram dois arquivos, somando 44 KB. As demais fontes foram examinadas e este documento registra o que cada uma ainda oferece, com a medição feita sobre os arquivos, e não sobre a expectativa.

## 2. RENAEST, com 455 arquivos e 27 GB

O conjunto tem quatro tabelas que se ligam pelo número do acidente. A de acidentes traz a unidade da federação, o ano, o quilômetro da via, a latitude, a longitude, o tipo de rodovia e os atributos da via: pavimento, limite de velocidade, tipo de pista, existência de guardrail, canteiro central e acostamento. A de vítimas traz a faixa etária, o gênero, o tipo de envolvido e a gravidade da lesão. A de tipo de veículo traz a contagem por categoria. A de localidade traz a frota total e a frota circulante do município.

A medição do preenchimento, sobre 400 mil linhas, corrige uma leitura anterior. Os campos estão preenchidos em 100%, e a lacuna aparece como categoria explícita: no tipo de rodovia, 29% dos registros trazem "não informado" e 16% trazem "desconhecido", restando 55% com valor útil, dos quais 35% são municipais, 10% federais e 9% estaduais. Na gravidade da lesão, 30% são "não informado" e 18% "desconhecido", restando 52% com valor útil.

**O que rende.** As três tabelas juntas formam o mesmo vetor C que o modelo de custo consome: ocorrência, vítimas por gravidade e veículos por tipo. Isso permite calcular o custo social das rodovias estaduais e municipais pelo mesmo método aplicado às federais, substituindo os fatores de 1,6 a 1,97 que o IPEA usa para essa parcela, e que o próprio relatório de 2006 descreve, na fração municipal, como escolhidos "de forma totalmente arbitrária". É o maior ganho metodológico disponível para o artigo nacional.

**O que custa.** A leitura são 4,4 GB entre as três tabelas principais, com agregação por unidade da federação, ano e gravidade. O processamento é viável em uma passagem, na ordem de dezenas de minutos. O trabalho de método é maior que o de código: decidir o tratamento dos 45% sem tipo de rodovia e dos 48% sem gravidade, o que exige regra de imputação declarada e análise de sensibilidade.

**O que não rende.** Nada para o piloto do Rio Grande do Norte. O documento de controle da LAI registra que o estado não preenche a gravidade no RENAEST, e o mapa de trechos críticos usa a malha federal, que já vem da PRF.

## 3. SIH com valor monetário: indisponível localmente

A pasta traz dois agregados de internação e dois scripts de coleta. Os agregados têm apenas a contagem, por unidade da federação, ano e mês. Nenhum arquivo local contém o valor da autorização de internação, os dias de permanência ou os dias de unidade de terapia intensiva.

**O que rende.** Substituir o componente hospitalar do vetor M, que hoje vem de uma fórmula de 2001 corrigida por IPCA, pelo valor efetivamente pago. É o segundo maior componente do custo, com 19,6% do total, e a substituição responde à recomendação do próprio Texto para Discussão 2565 de renovar os custos unitários.

**O que custa.** A obtenção depende de nova coleta no DATASUS, o que está fora do alcance imediato. A tarefa é de download e reprocessamento, não de análise, e o script de coleta já existe na pasta.

## 4. SAMU: sem valor recuperável

A medição encerra a dúvida. No arquivo do Rio Grande do Norte, das 6.952 linhas de produção ambulatorial, apenas duas trazem valor aprovado, somando R$ 7.963,62 para 707.215 atendimentos, o que dá R$ 0,01 por atendimento. O código de diagnóstico está zerado em todas as linhas.

A causa é estrutural, e não de coleta: o atendimento do SAMU entra no Sistema de Informações Ambulatoriais sem valor unitário, porque o serviço é custeado por repasse em bloco. O agregado com valor zerado, que parecia erro de processamento, reflete o dado de origem.

**Conclusão.** O componente pré-hospitalar observado não é obtenível por esta via. Ele permanece com o valor do IPEA, e a alternativa é a razão entre o repasse federal de custeio e o número de atendimentos, que exige outra fonte.

## 5. Microdado do SIM: granularidade incompatível

As pastas de saúde reúnem 410 arquivos e 7,5 GB, entre o formato comprimido do DATASUS e os extratos em CSV. O microdado traz o município de ocorrência, o local do óbito e a causa básica, e não traz a rodovia nem o quilômetro.

**O que rende.** Uma correção de subregistro por município, mais fina que a atual por unidade da federação. E, com o local de ocorrência, a possibilidade de estabelecer o fator de subregistro com origem própria, que a auditoria da planilha V07 apontou como pendência.

**O que custa.** A descompressão do formato do DATASUS e o cruzamento por município. O ganho não chega ao mapa, porque sem rodovia e quilômetro o registro não ancora em segmento.

## 6. Demais pastas

A pasta de custo social reúne as sete versões da planilha de parâmetros e os memoriais. A V07 já foi auditada e as suas correções estão registradas; não há dado novo a ingerir. A pasta da PRF traz o extrato antigo do Rio Grande do Norte, descartado por inflar as vítimas em 187%, e substituído pela reconstrução a partir dos arquivos anuais nacionais.

## 7. Comparação

| Fonte | Custo | Ganho no piloto RN | Ganho no artigo nacional | Situação |
|---|---|---|---|---|
| RENAEST | alto: 4,4 GB e regra de imputação | nenhum | alto: substitui os fatores arbitrários do IPEA | disponível |
| SIH com valor | médio: nova coleta | médio: refina o componente hospitalar | alto: renova o custo unitário | indisponível localmente |
| SAMU | baixo | nenhum | nenhum | encerrado, sem valor na origem |
| Microdado do SIM | médio: descompressão e cruzamento | nenhum | médio: subregistro por município | disponível |
| Planilhas e extrato antigo | nulo | nenhum | nenhum | encerrados |

## 8. Recomendação

A prioridade dos quatro dias restantes é a camada de aplicação, e não a ingestão. A rubrica da disciplina atribui 2,0 pontos ao sistema completo com dez requisitos funcionais e 1,0 ponto à demonstração ao vivo, e os três requisitos ainda abertos são a consulta web com mapa, os relatórios estruturados e a consulta em linguagem natural. Nenhuma das fontes pendentes acrescenta requisito funcional, e o banco já entrega o que a aplicação precisa consumir.

O RENAEST é a melhor das fontes pendentes, e o momento dele é depois da apresentação. Ele não altera o piloto, exige decisão de método sobre quase metade dos registros e rende justamente no artigo nacional, cujo prazo é outro. Antecipá-lo consumiria o tempo da demonstração para produzir um resultado que a banca não vai avaliar.

O SIH com valor entra na mesma janela do RENAEST, com a coleta refeita. O SAMU sai do plano, com a razão documentada. O microdado do SIM fica como terceira prioridade, para o fator de subregistro com origem própria.

A ordem proposta é: concluir a aplicação até 12 de setembro; depois RENAEST, depois SIH com valor, depois microdado do SIM.
