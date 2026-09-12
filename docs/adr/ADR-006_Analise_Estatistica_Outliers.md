# ADR-006 - Analise estatistica e deteccao de outliers

Formato MADR. Numeracao propria da sandbox da disciplina.

- Status: ACEITO
- Data: 2026-09-09
- Decisor: Bruno dos Santos Fernandes da Silva
- Relaciona-se com: ADR-003 (monolito modular), ADR-005 (camada canonica)

## Contexto

Os dados consolidados precisam de uma analise descritiva reproduzivel. Valores
invalidos nao podem contaminar as metricas, e observacoes extremas precisam ser
sinalizadas sem serem apagadas automaticamente.

## Decisao

A analise sera somente leitura sobre a camada canonica. Para cada coluna
numerica, o relatorio deve informar quantidade valida e invalida, media,
mediana e desvio padrao amostral. Valores vazios ou nao numericos ficam fora
das metricas e permanecem contabilizados como invalidos.

A deteccao de outliers usara o criterio IQR: abaixo de Q1 - 1,5 IQR ou acima
de Q3 + 1,5 IQR. O sistema sinaliza valor e identificador da observacao, mas
nao remove, altera ou substitui o registro.

## Consequencias

Os resultados sao comparaveis entre execucoes e preservam o dado original. A
interpretacao do outlier continua sendo responsabilidade analitica. Mudancas
na definicao estatistica exigem nova versao do contrato do relatorio.

## Alternativas consideradas

Remover outliers automaticamente foi rejeitado por destruir evidencia. Usar
somente media e desvio padrao foi rejeitado por ser sensivel a extremos. Usar
um limite fixo por coluna foi rejeitado porque nao se adapta a distribuicoes
diferentes.

## Verificacao

Testes devem cobrir metricas conhecidas, valores invalidos, outlier acima ou
abaixo do limite e ausencia de alteracao na tabela.
