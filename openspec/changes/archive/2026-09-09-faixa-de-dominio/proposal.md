# Proposta - Limpeza geodesica pela faixa de dominio

## Por que

Parte dos sinistros aparece no mapa longe do leito da rodovia, as vezes a
quilometros do eixo. Sao erros de coordenada: o acidente e real e foi ancorado
pelo quilometro, mas a latitude e a longitude do boletim estao corrompidas. No
mapa, esses pontos poluem o tracado e sugerem sinistro onde nao houve.

Medida contra o eixo da BR, com a geometria oficial do DNIT, a distancia mostra
que 95% dos sinistros estao a ate 41 metros da via, e 4,2% caem fora de uma faixa
de 50 metros para cada lado.

## O que muda

Um script mede a distancia de cada sinistro ao eixo da sua BR e grava uma marca de
qualidade no banco: dentro ou fora da faixa de dominio de 50 metros. O mapa passa a
desenhar apenas os sinistros de dentro da faixa.

## Fora de escopo

A marca nao altera o custo nem a contagem por segmento. O sinistro fora da faixa
continua no calculo, porque o acidente e real e a ancoragem usa o quilometro, e nao
a coordenada. A limpeza e da visualizacao, e a marca fica declarada no banco.
