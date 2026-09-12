# Proposta - Geometria oficial do SNV no mapa

## Por que

O mapa desenha cada trecho ligando os seus sinistros em ordem de quilometro,
porque o banco nao guarda a geometria da via. Com os sinistros esparsos, essa
linha cruza o estado e polui o mapa, sem representar o tracado real.

A base geometrica do DNIT traz a polilinha oficial de cada trecho, com o mesmo
codigo de segmento que o nosso banco usa. Ela resolve o problema na origem.

## O que muda

Um script de ingestao le a base geometrica do SNV, filtra a unidade da federacao,
simplifica cada tracado e grava numa tabela do banco consolidado. A consulta passa
a devolver o tracado oficial, e recua para a aproximacao por sinistros apenas nos
trechos sem geometria.

## Fora de escopo

A ingestao nao altera o custo nem a criticidade. O desenho usa uma safra de
referencia, enquanto o custo continua ancorado na safra do ano do sinistro. A base
bruta do DNIT permanece fora do controle de versao; so o tracado simplificado, de
poucas dezenas de quilobytes, entra no banco.
