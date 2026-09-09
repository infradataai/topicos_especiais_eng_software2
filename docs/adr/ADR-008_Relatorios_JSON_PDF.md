# ADR-008 - Relatorios estruturados em JSON e PDF

Formato MADR. Numeracao propria da sandbox da disciplina.

- Status: ACEITO
- Data: 2026-09-09
- Decisor: Bruno dos Santos Fernandes da Silva
- Relaciona-se com: ADR-003 (monolito modular), ADR-005 (proveniencia), ADR-006 (analise)

## Contexto

Os resultados de qualidade, estatistica, outliers e origem precisam ser
consumidos por sistemas e por pessoas. A exportacao deve representar o mesmo
resultado nos formatos estruturado e legivel.

## Decisao

Adotar uma representacao interna validada como fonte unica para as exportacoes.
O JSON sera a representacao estruturada, com versao do esquema, periodo,
metricas, alertas e metadados de fonte, lote e versao. O PDF apresentara as
mesmas informacoes essenciais nas secoes de resumo, qualidade, analise e
proveniencia.

A geracao sera deterministica para a mesma entrada e somente leitura em
relacao ao banco. Falha de validacao ou serializacao deve interromper a
exportacao com erro descritivo, sem alterar dados.

## Consequencias

Integracoes podem consumir JSON e usuarios podem arquivar ou compartilhar PDF.
A versao do esquema precisa ser mantida para compatibilidade. A biblioteca de
PDF fica encapsulada no modulo de relatorios para nao contaminar ingestao e
analise.

## Alternativas consideradas

Gerar JSON e PDF por caminhos independentes foi rejeitado porque permite
resultados divergentes. Exportar somente PDF foi rejeitado por dificultar
integracao automatica. Gravar o relatorio no banco durante a exportacao foi
rejeitado para preservar a separacao entre dados e artefatos derivados.

## Verificacao

Testes devem validar o esquema JSON, campos de proveniencia, resultado vazio,
conteudo essencial do PDF, determinismo e ausencia de alteracao no banco.
