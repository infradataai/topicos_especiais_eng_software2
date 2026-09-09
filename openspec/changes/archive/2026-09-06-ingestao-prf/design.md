# Design — ingestão e normalização da PRF

## Contexto técnico

O arquivo anual da PRF tem 37 colunas e mistura três granularidades na mesma linha: atributos da ocorrência, do veículo e da pessoa, mais a causa e o tipo do acidente. A repetição por causa e tipo é o que multiplica as linhas. Sete arquivos somam cerca de 1,4 GB, o que exige leitura em blocos.

## Decisões

**Separar por grão, em vez de deduplicar a linha inteira.** A alternativa de aplicar uma deduplicação sobre a linha completa não resolveria, porque as linhas repetidas diferem justamente nas colunas de causa e tipo. Separar em quatro tabelas, cada uma com a sua chave, resolve a contagem e preserva a informação de causa. Esta decisão vai para ADR próprio, por ser estrutural.

**Reconhecer a data por padrão, sem inferência.** A alternativa de fixar `dayfirst=True` para toda a série quebraria os anos em `AAAA-MM-DD`. A alternativa de inferir por arquivo funcionaria hoje, mas falharia no dia em que um arquivo trouxesse formatos misturados. Reconhecer cada valor pelo seu padrão é determinístico e sobrevive à mistura. Segue o princípio de determinismo de parsing já adotado na tese.

**Declarar a ausência em vez de nulificar.** O estado físico ausente vira `nao_informado`. A alternativa de deixar nulo esconde a lacuna no meio dos demais nulos técnicos e impede medir a completude.

**Falhar quando a chave de deduplicação não existir.** A alternativa de deduplicar por combinação aproximada de colunas produziria um número plausível e errado, que é pior que a falha.

## Leitura e memória

A leitura usa blocos de 200 mil linhas, com filtro por unidade da federação aplicado dentro do bloco, o que mantém o uso de memória proporcional ao tamanho da UF e não ao do arquivo. Todas as colunas entram como texto, e a conversão de tipo acontece depois da deduplicação, uma vez por registro.

## Interface

    ler_ano(caminho, uf) -> DataFrame bruto da UF
    normalizar(bruto)    -> {ocorrencias, veiculos, pessoas, causas_tipos}
    ingerir(origem, uf, anos) -> (tabelas, RelatorioIngestao)
    validar(tabelas)     -> lista de achados
    vetor_c(tabelas)     -> contagem por ocorrência

O consumidor a jusante recebe o vetor C e não conhece o formato de origem.

## Rastreabilidade

Cada cenário da spec tem um teste correspondente em `Projeto_Final/tests/test_ingestao_prf.py`. A evidência numérica que motivou os requisitos está em `Projeto_Final/docs/reconstrucao-e-auditoria-v07.md`.
