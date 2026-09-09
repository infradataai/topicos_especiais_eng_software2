# Design - Relatorios estruturados

## Decisoes

Uma representacao interna de relatorio e validada antes da exportacao. O JSON preserva tipos, metadados, metricas, alertas e proveniencia. O PDF apresenta as mesmas informacoes em secoes legiveis, com titulo, periodo, fonte e data de geracao.

A geracao recebe resultados ja calculados e e deterministica para a mesma entrada. Falhas de serializacao ou de geracao devem ser reportadas sem modificar o banco.

## Interface

`gerar_json(relatorio) -> str` e `gerar_pdf(relatorio, destino) -> Path`.
