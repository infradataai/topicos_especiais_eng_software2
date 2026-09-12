# Desenho - Geometria oficial do SNV

## Fonte e casamento

A base geometrica do DNIT, no formato shapefile, traz uma polilinha por trecho, no
campo `vl_codigo`, identico ao `codigo` do nosso banco. Na safra 202507A, 169 dos
171 segmentos do Rio Grande do Norte casam pelo codigo. Os dois restantes,
recodificados entre safras, recuam para a aproximacao por sinistros.

## Coordenadas

As coordenadas vem em graus, no SIRGAS 2000, que para desenho equivale ao WGS 84.
Entram na biblioteca de mapa sem reprojecao. O arquivo de projecao acompanha vazio,
e a faixa de valores confirma o sistema geografico.

## Simplificacao

Cada tracado passa por Douglas-Peucker com tolerancia de cerca de 90 metros, abaixo
do que se distingue na escala do estado. No Rio Grande do Norte, os 97 mil pontos
brutos caem para cerca de 900, uma reducao de 99%, e o conjunto ocupa 40 quilobytes.

## Safra de referencia

O desenho usa uma safra fixa, a 202507A, porque a via quase nao se move entre
safras. O custo e a criticidade seguem ancorados na safra do ano do sinistro, como
antes. So o tracado no mapa vem da safra de referencia.

## Onde a geometria fica

A geometria entra numa tabela do banco consolidado, `geometria_segmento`, com o
codigo, a safra e a lista de pontos em texto JSON. Assim ela viaja junto do banco de
8,5 megabytes, sem depender dos 88 megabytes da base bruta, que ficam no repositorio
privado, fora do git.

## Recuo

A consulta le a geometria oficial e, para o trecho sem ela, devolve a aproximacao por
sinistros. O mapa continua desenhavel em qualquer unidade da federacao, mesmo antes
de a geometria ser ingerida.
