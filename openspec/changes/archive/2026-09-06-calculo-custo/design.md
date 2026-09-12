# Design — cálculo do custo social por ocorrência

## Estrutura do vetor M

O vetor M é uma tabela de três dimensões: o componente (linha), a gravidade da ocorrência (coluna) e o bloco a que pertence (pessoas, veículos ou institucional). Ele é dado de configuração, não lógica, e fica declarado em módulo próprio, com a fonte anotada em cada bloco. Os valores entram a preços de dezembro de 2014, como publicados na Tabela 1 do TD 2565, e o deflator é aplicado ao final.

A representação escolhida é um dicionário indexado por chave composta, em vez de uma matriz posicional, porque o índice legível (`("obito", "com_fatalidade")`) sobrevive a uma reordenação da tabela e falha de forma clara quando a chave não existe.

## Separação entre contagem e valoração

A contagem de veículos por classe, com a regra de composição, fica numa função própria, separada da valoração. A razão é que a regra de composição é a parte com condicional e a que concentra o risco de erro, e mantê-la isolada permite testá-la sem envolver dinheiro. A valoração recebe as contagens já resolvidas e faz apenas multiplicação e soma.

## A regra de composição

    tratoras = n(Caminhão) + n(Caminhão-trator)
    carretas = n(Semirreboque) + n(Reboque)

    n(Caminhões) = tratoras            se tratoras > 0
    n(Caminhões) = 1                   se tratoras = 0 e carretas > 0
    n(Caminhões) = 0                   caso contrário

O segundo ramo cobre a carreta cujo cavalo mecânico não foi registrado, e o primeiro absorve o bitrem, em que uma tratora puxa duas carretas. As três situações têm cenário próprio na spec.

## Falhar em vez de supor

Duas situações levantam exceção em vez de adotar um valor por omissão: a classificação de acidente fora das três previstas e o tipo de veículo ausente da tabela de mapeamento. A segunda importa porque a classe Outros do IPEA custa R$ 79.931,58 no acidente com vítimas, mais que o caminhão, e absorver o desconhecido nela inflaria o resultado em silêncio. A dívida de estender o mapeamento às demais unidades da federação, registrada no ADR-008, se manifesta como essa exceção quando o cálculo rodar em outro estado.

## Interface

    custo_pessoas(contagem_por_gravidade, gravidade_ocorrencia) -> float
    contar_caminhoes(contagem_por_tipo) -> int
    custo_veiculos(contagem_por_tipo, gravidade_ocorrencia) -> float
    custo_institucional(gravidade_ocorrencia) -> float
    custo_ocorrencia(vetor_c, gravidade_ocorrencia) -> ResultadoCusto

O `ResultadoCusto` carrega o total, os três subtotais, a contagem de pessoas sem gravidade e a categoria da ocorrência, para que a decomposição não precise ser recalculada a jusante.

## Ordem da atualização monetária

O deflator multiplica o total da ocorrência, e não cada componente. As duas ordens dão o mesmo número, por distributividade, mas multiplicar uma vez reduz o acúmulo de arredondamento e deixa um único ponto onde a base monetária é aplicada, o que facilita trocá-la.

## Rastreabilidade

Cada cenário da spec tem um teste correspondente em `tests/test_custo_social.py`. O exemplo trabalhado da ocorrência 182341, com total de R$ 1.682.487,58, entra como teste de regressão de número fechado, e trava a memória de cálculo inteira: qualquer mudança no vetor M, no mapeamento, na regra de composição ou no deflator quebra esse teste.
