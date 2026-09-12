# Proposta — Ingestão e normalização dos microdados de sinistros da PRF

## Por quê

O cálculo do custo social pelo modelo aditivo do IPEA exige contar, em cada ocorrência, quantas pessoas houve por gravidade e quantos veículos por tipo. Esse é o vetor C do produto escalar C · M. O conjunto que a PRF publica, "todas as causas e tipos", não serve a essa contagem no formato em que chega: ele repete a mesma pessoa uma vez para cada combinação de causa e tipo do acidente. Contar linha a linha infla as vítimas.

A medição no extrato do Rio Grande do Norte quantificou o efeito: 1.570 óbitos contados linha a linha contra 547 reais no mesmo período, uma inflação de 187%; os feridos graves inflam 122% e os leves 123%.

Um segundo problema apareceu na leitura da série. O arquivo de 2022 traz a data no formato `DD/MM/AAAA`, enquanto os demais anos usam `AAAA-MM-DD`. Sob inferência automática de formato, as datas cujo dia passa de 12 são descartadas em silêncio e as demais têm dia e mês trocados. O efeito medido foi a perda de 791 das 1.288 ocorrências de 2022, exatamente a fração 12/31 que a regra prevê.

Sem uma ingestão que resolva os dois problemas, todo cálculo a jusante herda o erro.

## O que muda

Adiciona um módulo de ingestão que lê os arquivos anuais da PRF, filtra pela unidade da federação, e normaliza o conteúdo em quatro tabelas de grão único: ocorrências, veículos, pessoas e pares de causa e tipo. A deduplicação usa as chaves próprias de cada grão. O reconhecimento de data trata cada formato pelo seu próprio padrão, sem inferência. A ausência de estado físico vira categoria declarada. Um validador confere a consistência entre as contagens por gravidade e os indicadores do próprio arquivo, e uma função monta o vetor C por ocorrência.

## Fora de escopo

A valoração monetária, que consome o vetor C e pertence ao módulo de custo. A ancoragem no segmento do SNV, que pertence ao módulo de referenciamento. A correção de subregistro e a reclassificação de gravidade, que são decisões de método e entram a jusante. A ingestão de fontes que não sejam a PRF, tratada em mudanças próprias.

## Origem do conhecimento

Os requisitos desta proposta vieram de um spike de descoberta sobre os dados reais, e não de uma antecipação teórica. O defeito de formato de data de 2022 não seria previsível sem a leitura do arquivo. O spike está documentado em `Projeto_Final/docs/reconstrucao-e-auditoria-v07.md`, e o caso de borda que ele revelou entra nesta spec como critério de aceite.
