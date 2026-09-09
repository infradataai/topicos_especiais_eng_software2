# Desenho - Mapa dos trechos críticos

## Onde fica o SQL

O módulo `custo_social_core/consultas.py` concentra as consultas do esquema de
sinistros e devolve listas de dicionários. Ele usa `sqlite3` da biblioteca padrão, e
não o SQLAlchemy do `persistencia.py`, porque a camada web recebe uma
`sqlite3.Connection` e a fronteira de aplicação não deve carregar o mapeador.

## Banco sem as tabelas de sinistro

A mesma aplicação serve ao banco da LAI, que não tem as tabelas do núcleo. As rotas
novas verificam a presença das tabelas antes de consultar e respondem 400 com mensagem
explícita, em vez de deixar vazar o erro do SQLite. A verificação usa
`sqlite_master`, e não uma consulta de teste.

## As duas leituras de criticidade

O custo por quilômetro divide o custo agregado pela extensão do segmento. O custo por
veículo-quilômetro divide o mesmo custo pela exposição anual, dada por volume médio
diário anual vezes extensão vezes 365. Os dois ranques divergem, e o mapa mostra os
dois, porque a escolha entre eles é decisão de política pública e não do sistema. O
segmento sem volume medido recebe nulo na segunda leitura, e permanece na primeira.

## Junção por código e safra

A tabela `segmentos_snv` tem chave composta por safra e código. Juntar só pelo código
multiplica o custo pelo número de safras ancoradas. A consulta usa a safra mais recente
de cada segmento, como já faz o `persistencia.custo_por_segmento`.

## Mapa

A página usa a Leaflet a partir de rede pública, com a camada base do OpenStreetMap. O
carregamento da biblioteca é verificado, e a página mostra aviso quando a rede não está
disponível, mantendo a tabela de segmentos utilizável.
