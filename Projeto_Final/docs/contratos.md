# Contratos do núcleo (EARS)

Cada módulo do núcleo declara o seu contrato em notação EARS, para que a implementação da fase 2 seja rastreável até uma regra verificável. Os identificadores de código ficam em inglês; a prosa, em português, pela convenção do ADR-009.

## referenciamento

QUANDO um sinistro tem `br`, `uf` e `km`, o sistema DEVE ancorá-lo ao segmento do SNV cuja faixa `[km_inicial, km_final]` contém o `km`, na mesma BR e UF. QUANDO o ano do sinistro é informado, o sistema DEVE usar a safra do SNV vigente naquele ano. SE nenhum segmento contiver o `km`, o sistema DEVE sinalizar `ForaDaFaixa`, sem aproximar.

## custo

QUANDO uma ocorrência é sem vítimas, o custo DEVE ser o valor de dano material. QUANDO uma ocorrência tem feridos, o custo DEVE somar o custo de cada vítima por gravidade, e a soma DEVE reproduzir a classe de feridos do Ipea dentro da tolerância de triangulação. QUANDO uma ocorrência tem óbito, o custo DEVE somar o valor por vítima fatal. O refino DECOMPÕE a classe de feridos do Ipea; ele não soma sobre o valor do Ipea.

## exposicao

QUANDO o segmento tem VMDa e extensão, o sistema DEVE calcular o custo por veículo-km do ano. SE o segmento não tem posto de contagem, o sistema DEVE marcar a exposição como imputada, e a imputação DEVE aparecer no resultado.

## subregistro

QUANDO um valor observado e um cenário são dados, o sistema DEVE devolver o valor corrigido pelo fator do cenário. O cenário DEVE ser um dos declarados em `config.FATOR_SUBREGISTRO`: piso, central ou teto.

## pipeline

QUANDO uma UF é informada, o sistema DEVE processar apenas os sinistros daquela UF e DEVE destacar como corredor as BRs listadas em `config.CORREDORES_POR_UF` para a UF. A troca de UF é o único parâmetro que separa o piloto RN da escala nacional.
