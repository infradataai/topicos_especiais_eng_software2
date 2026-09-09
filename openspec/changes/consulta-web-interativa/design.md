# Design - Consulta web interativa

## Decisoes

A aplicacao expoe endpoints de consulta parametrizados sobre o banco consolidado e uma tela web que consome esses endpoints. Filtros e ordenacao sao transformados em parametros vinculados; SQL recebido diretamente do usuario e rejeitado.

As respostas devem ser paginadas, indicar a origem dos dados e informar quando nao houver resultados. A interface e somente leitura para preservar a ingestao e a proveniencia.

## Interface

`GET /api/registros`, `GET /api/fontes` e `GET /api/lotes`, com filtros documentados e limite de pagina configurado.
