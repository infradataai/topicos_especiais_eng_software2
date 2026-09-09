# Proposta — Ingestão da exposição de tráfego (PNCT/VMDa) e dos dados de saúde (DATASUS)

## Por quê

O custo por quilômetro já existe, e ele responde onde o dinheiro se perde. Ele não responde onde a via é perigosa. Um trecho caro pode ser apenas movimentado: a BR-101 na entrada de Natal concentra custo porque passa muito veículo, e não necessariamente porque mata mais por veículo que passa. Separar as duas leituras exige o denominador de exposição, e é o Plano Nacional de Contagem de Tráfego que o fornece.

O segundo motivo é a correção do subregistro. A auditoria da planilha V07 mostrou que o teto de 1,96 media a razão entre o total de óbitos por transporte e a parcela ocorrida em via pública, que é outra coisa. Corrigir isso exige os óbitos do Sistema de Informações sobre Mortalidade por unidade da federação e ano, que estão no DATASUS. As internações do Sistema de Informações Hospitalares entram no mesmo movimento, como lastro da completude do registro de ferido grave.

As duas ingestões entram juntas porque ambas gravam no banco já consolidado e ambas se agregam à mesma unidade de análise.

## O que muda

Adiciona a ingestão do VMDa, que traz o volume médio diário anual por segmento da malha. A junção com os segmentos do SNV é direta, porque o arquivo do PNCT carrega o mesmo código de segmento. A partir dele, o sistema calcula a exposição anual em veículos-quilômetro e a criticidade por exposição de cada trecho.

Adiciona a ingestão dos agregados do DATASUS: os óbitos por acidente de transporte por unidade da federação e ano, com a abertura entre óbito em estabelecimento de saúde e em via pública, e as internações por causa externa por unidade da federação, ano e mês.

## Fora de escopo

A substituição do componente hospitalar do vetor M pelo valor observado no SIH, que exige a extração dos campos monetários e entra como variante própria. O custo do atendimento pré-hospitalar do SAMU. O microdado do SIM por município, que não tem referenciamento por rodovia e quilômetro e por isso não ancora em segmento.

## O que a leitura das fontes revelou

O arquivo do VMDa muda o nome da aba de dados a cada ano: `SNV_201903A` em 2018, `VMDa 2021` em 2021, `VMDa2025_SNV202401A` em 2025. A leitura não pode depender de nome fixo.

O mesmo segmento aparece mais de uma vez no arquivo, com valores de tráfego diferentes: são 8.222 linhas para 5.776 códigos distintos na safra de 2024, e um único código chega a ter dez valores distintos de VMDa. São postos de contagem diferentes no mesmo trecho, e a agregação precisa de regra declarada.

Os arquivos agregados do DATASUS trazem marca de ordem de byte no início do cabeçalho, o que faz a primeira coluna ser lida com um caractere invisível no nome. É o terceiro caso de heterogeneidade de formato encontrado no projeto, depois da data da PRF de 2022 e da vírgula decimal do SNV de novembro de 2025.
