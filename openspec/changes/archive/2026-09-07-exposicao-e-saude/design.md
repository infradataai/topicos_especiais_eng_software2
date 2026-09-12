# Design — exposição de tráfego e dados de saúde

## Junção do VMDa com os segmentos

O arquivo do PNCT carrega a coluna `vl_codigo`, que é o mesmo código de segmento do SNV. A junção é por igualdade de código, sem casamento espacial e sem tolerância de quilometragem. Isso elimina a classe de erro mais comum nesse tipo de integração.

A safra do SNV a que cada arquivo anual do VMDa se refere aparece no nome da aba e na coluna `versao_snv`, e nem sempre coincide com a safra usada na ancoragem dos sinistros daquele ano. Como o código do segmento é estável entre safras próximas, a junção usa o código e registra a safra de origem do VMDa, para que a diferença fique visível em vez de silenciosa.

## Agregação de postos

O mesmo código aparece até dez vezes com volumes diferentes, porque há mais de um posto de contagem no trecho. A média foi escolhida por representar o tráfego típico ao longo do segmento, que é o que a exposição em veículos-quilômetro pede.

O máximo foi considerado e descartado: ele descreveria o ponto mais movimentado, o que serviria a um estudo de capacidade, e não à exposição média. A soma foi descartada de imediato, porque contaria o mesmo fluxo mais de uma vez.

O número de postos agregados fica registrado, para que a incerteza do segmento seja legível.

## Sentidos e ausências

O volume total do segmento é a soma dos dois sentidos. Quando um sentido falta, o presente é usado e a incompletude é registrada, porque descartar o segmento inteiro perderia informação de tráfego que existe. Quando os dois faltam, a exposição é nula declarada, e o segmento continua no ranque por custo por quilômetro, apenas sem a leitura por exposição. Imputar tráfego em silêncio produziria uma criticidade inventada.

## Cobertura de jurisdição, e não subregistro

A razão entre os óbitos da PRF e os do SIM é calculada e nomeada como cobertura de jurisdição. A auditoria da planilha V07 mostrou o risco de confundir as duas coisas: o teto de 1,96 daquela planilha vinha da razão entre o total de óbitos por transporte e a parcela ocorrida em via pública, que descreve onde a vítima morreu, e não o que a polícia deixou de registrar.

O módulo recusa devolver a cobertura quando ela é pedida como fator de subregistro. A recusa é deliberada: é mais barato falhar do que deixar o número circular com o rótulo errado, como já aconteceu.

## Interface

    exposicao.ler_vmda(caminho)              -> DataFrame por posto
    exposicao.agregar_por_segmento(df)       -> DataFrame por codigo, com n_postos
    exposicao.veiculos_km_ano(vmda, ext)     -> float
    exposicao.criticidade(custo, vmda, ext)  -> float | None

    saude.ler_agregado(caminho)              -> DataFrame sem marca de ordem de byte
    saude.cobertura_jurisdicao(prf, sim)     -> DataFrame rotulado

## Rastreabilidade

Cada cenário das duas specs tem um teste correspondente, em `tests/test_exposicao.py` e `tests/test_saude.py`.
