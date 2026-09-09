# Proposta - Mapa dos trechos críticos

## Por que

A consulta web hoje enxerga apenas o esquema da LAI, com as tabelas `fontes`, `lotes` e
`registros_canonicos`. O banco consolidado guarda o resultado do projeto em outras onze
tabelas: ocorrências da PRF, custo por ocorrência, segmentos do SNV, ancoragem e
exposição. Sem rotas para essas tabelas, a aplicação mostra as cargas de dados e não os
sinistros analisados.

O requisito da disciplina pede consulta web com mapa dos trechos críticos. O dado
necessário já está no banco: cada ocorrência traz latitude, longitude e custo social, e
cada segmento traz extensão, volume médio diário anual e custo agregado.

## O que muda

Acrescenta três rotas somente leitura à aplicação de consulta, sob o ADR-007: uma lista
de segmentos ordenável pelas duas leituras de criticidade, uma lista paginada de
ocorrências com coordenada e custo, e uma página de mapa que projeta as duas camadas.

As consultas ficam num módulo próprio do núcleo, `custo_social_core/consultas.py`, de
modo que a camada web não escreva SQL do esquema de sinistros.

## Fora de escopo

A rota não recalcula custo, não altera o banco e não aceita SQL do cliente. A camada de
subnotificação não entra no mapa, porque o ADR-012 registra que o eixo 2 não tem fonte
medida.
