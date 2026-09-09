# Desenho - Faixa de dominio

## O que se mede, e contra o que

A faixa de dominio e uma corredor de 50 metros para cada lado do eixo da rodovia. O
teste mede a distancia de cada sinistro ao eixo da sua BR, e nao ao segmento
ancorado. A escolha da BR inteira, e nao do segmento, cobre o caso do sinistro cuja
coordenada cai num ponto correto da BR mas fora do trecho do seu quilometro, e cobre
os trechos sem geometria propria, cujo sinistro ainda tem a geometria da BR.

## Geometria cheia, nao a simplificada

A distancia se mede contra a geometria cheia do shapefile, e nao contra a versao
simplificada que o mapa desenha. A simplificacao afasta a linha do eixo em ate 90
metros, acima do limiar de 50, e usa-la inverteria o teste. Por isso o script le o
shapefile, e nao a tabela de geometria do banco.

## Metrica em metros

As coordenadas estao em graus. O script projeta para metros por uma aproximacao
equiretangular, com a longitude corrigida pelo cosseno da latitude de referencia do
estado. Para a extensao do Rio Grande do Norte, o erro dessa projecao e desprezivel
diante do limiar de 50 metros.

## Onde a marca fica

A marca entra numa tabela do banco, `qualidade_geo`, com o identificador do sinistro,
a BR, a distancia em metros e o indicador de dentro da faixa. A consulta do mapa
junta essa tabela e filtra os de dentro. Quando a marca ainda nao foi calculada, a
consulta devolve todos, para o mapa nao ficar vazio.

## O que nao muda

O custo por ocorrencia, o custo por segmento e a contagem de ocorrencias por segmento
seguem sobre todos os sinistros ancorados. A marca governa apenas a camada de pontos
do mapa.
