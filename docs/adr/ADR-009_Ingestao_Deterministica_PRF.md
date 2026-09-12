# ADR-009 — Ingestão determinística e normalização por grão dos microdados da PRF

Formato MADR. Numeração própria da sandbox da disciplina.

- Status: ACEITO
- Data: 2026-09-07
- Decisores: Flávio Eduardo Batista Moreira e Bruno dos Santos Fernandes da Silva
- Relaciona-se com: ADR-003 (monólito modular), ADR-004 (topologia de repositórios)
- Spec correspondente: `openspec/changes/ingestao-prf/`

## Contexto

O modelo aditivo de custo do IPEA calcula o custo de um acidente pelo produto escalar entre o vetor C, que conta as pessoas por gravidade e os veículos por tipo daquela ocorrência, e o vetor M de custos médios padrão. Montar o vetor C exige contar pessoas e veículos sem repetição.

O conjunto que a PRF publica, "todas as causas e tipos", mistura três granularidades na mesma linha e repete a pessoa uma vez para cada combinação de causa e tipo do acidente. A medição no extrato do Rio Grande do Norte quantificou o efeito de contar linha a linha: 1.570 óbitos contra 547 reais no mesmo período, uma inflação de 187%, com 122% nos feridos graves e 123% nos leves.

A leitura da série revelou um segundo problema. O arquivo de 2022 traz a data em `DD/MM/AAAA`, enquanto os demais anos usam `AAAA-MM-DD`. Sob inferência automática, as datas cujo dia passa de 12 viram nulo e as demais têm dia e mês trocados. A perda medida foi de 791 das 1.288 ocorrências de 2022, exatamente a fração 12/31 que a regra prevê.

Uma terceira lacuna apareceu na conferência: 9,1% das pessoas chegam sem estado físico, entre o valor "Não Informado" e o campo vazio.

## Decisão

**Normalizar em quatro tabelas de grão único, com chave própria.** As ocorrências são deduplicadas por `id`, os veículos por `(id, id_veiculo)`, as pessoas por `(id, pesid)` e os pares de causa e tipo por `(id, causa_acidente, tipo_acidente)`. A informação de causa e tipo migra para a tabela própria em vez de ser descartada. O vetor C é contado sobre pessoas e veículos, nunca sobre o arquivo bruto.

**Reconhecer a data pelo padrão de cada valor, sem inferência.** Os formatos `AAAA-MM-DD` e `DD/MM/AAAA` são identificados por expressão regular e convertidos com o formato explícito correspondente. O que não casa com formato conhecido vira nulo declarado e é contabilizado pelo validador.

**Declarar a ausência de estado físico como categoria.** O valor ausente vira `nao_informado`, e não nulo.

**Falhar quando a chave de deduplicação não existir.** Sem `pesid`, `id_veiculo` ou `id`, a leitura levanta exceção em vez de deduplicar por aproximação.

## Alternativas consideradas

**Deduplicar a linha inteira.** Não resolve, porque as linhas repetidas diferem justamente nas colunas de causa e tipo, que é o que as multiplica. Descartada por não atacar a causa.

**Descartar as colunas de causa e tipo antes de deduplicar.** Resolveria a contagem, ao custo de perder a informação de causa, que a análise de segurança viária usa. Descartada por perda de informação.

**Fixar `dayfirst=True` para toda a série.** Corrigiria 2022 e quebraria os seis anos em formato ISO. Descartada.

**Inferir o formato por arquivo.** Funcionaria hoje e falharia no dia em que um arquivo trouxesse formatos misturados, sem aviso. Descartada por fragilidade.

**Deixar o estado físico ausente como nulo.** Esconderia a lacuna entre os nulos técnicos e impediria medir a completude. Descartada.

**Deduplicar por combinação aproximada de colunas, na falta de `pesid`.** Produziria um número plausível e errado, que é pior do que a falha explícita. Descartada.

## Consequências

Ganha-se a contagem correta do vetor C, que é a precondição de todo o cálculo a jusante, e a rastreabilidade de cada grão pela sua chave. Ganha-se a série completa de 2019 a 2025, com as datas todas reconhecidas, e uma medida explícita da completude do estado físico. A validação cruzada passa a confirmar, a cada execução, que a contagem por gravidade bate com os indicadores do próprio arquivo.

Perde-se a simplicidade de uma tabela única: o consumidor precisa juntar os grãos quando quiser atributos de níveis diferentes na mesma linha. O custo é aceitável, porque a junção é explícita e o erro de contagem que ela evita é grande.

Assume-se a dívida de mapear os 24 tipos de veículo da PRF para as sete classes do vetor M do IPEA, e de definir a regra de tratamento das pessoas com gravidade `nao_informado`. As duas estão registradas como tarefas pendentes na spec.

## Reversibilidade

Alta. As tabelas normalizadas são derivadas e podem ser regeradas a qualquer momento a partir dos arquivos anuais, que permanecem intocados. Mudar a regra de deduplicação ou de reconhecimento de data significa alterar o módulo e reexecutar a ingestão, sem migração de dado.

## Procedência

Os requisitos desta decisão vieram de um spike de descoberta sobre os dados reais, e não de antecipação teórica. O defeito de formato de data de 2022 não seria previsível sem a leitura do arquivo. A evidência numérica está em `Projeto_Final/docs/reconstrucao-e-auditoria-v07.md`, e os critérios de aceite derivados dela estão em `openspec/changes/ingestao-prf/specs/prf-ingestao/spec.md`.
