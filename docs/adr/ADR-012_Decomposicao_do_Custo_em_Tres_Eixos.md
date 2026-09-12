# ADR-012 — Decomposição do custo social em três eixos independentes

Formato MADR. Numeração própria da sandbox da disciplina.

- Status: ACEITO
- Data: 2026-09-07 (revisado no mesmo dia, ver "Histórico de revisão")
- Decisores: Flávio Eduardo Batista Moreira e Bruno dos Santos Fernandes da Silva
- Relaciona-se com: ADR-011 (parâmetros do cálculo), ADR-009 (ingestão determinística)
- Governa: a redação dos resultados e a ingestão de qualquer fonte nova

## Contexto

O cálculo entrega hoje o custo social da malha federal: R$ 1,915 bilhão no Rio Grande do Norte e R$ 100,44 bilhões no país, de 2019 a 2025, a preços de junho de 2026. Esse número é um piso, por três razões declaradas: as pessoas sem gravidade informada entram com custo zero, as ocorrências não ancoradas ficam de fora, e o próprio IPEA registra que os custos não valorados, como sofrimento e sequelas, permanecem excluídos, de modo que "os custos aqui encontrados são sempre menores do que os custos realmente incorridos".

A pergunta é como as fontes ainda não ingeridas completam esse número. A formulação intuitiva trata o conjunto como um intervalo entre piso e teto, e define a subnotificação como a diferença entre os dois. Essa formulação junta grandezas que se medem em eixos distintos.

O risco não é hipotético. A auditoria da planilha V07 encontrou exatamente esse erro em circulação: o teto de 1,96 vinha da razão entre o total de óbitos por transporte e a parcela ocorrida em via pública, e era aplicado como fator de subnotificação. A razão descreve onde a vítima morreu; ela nada diz sobre o que a polícia deixou de registrar. Um rótulo errado sobreviveu porque nenhuma decisão o fixava.

## Decisão

O custo social dos sinistros se decompõe em três eixos independentes, que não se somam entre si e não se substituem.

**Eixo 1, jurisdição.** O custo total do país é a soma de parcelas de universos distintos: a malha federal, a malha estadual e municipal, e as vias urbanas. São acidentes diferentes, em vias diferentes, sob autoridades diferentes. Cada parcela tem o seu próprio piso e o seu próprio teto. Acrescentar uma parcela amplia o universo medido, e NÃO revela omissão de registro em outra parcela.

**Eixo 2, subnotificação.** É o acidente que ocorreu dentro de uma jurisdição e não foi registrado pela autoridade daquela jurisdição. Na malha federal, a causa típica é a morte tardia: a vítima consta como ferido grave no boletim e falece depois, já no hospital.

**Eixo 3, completude do valor unitário.** É a qualidade do vetor M, e não a contagem de acidentes. Substituir um componente pelo valor observado corrige o preço do mesmo evento, e pode tanto elevar quanto reduzir o resultado.

Disso decorrem três regras de escrita e de cálculo.

O teto federal é o piso federal mais a subnotificação federal mais os componentes não valorados. Nada além disso entra nessa conta.

A subnotificação é sempre medida dentro da mesma jurisdição, contra uma fonte que cubra a mesma malha e que seja pelo menos tão completa quanto a fonte auditada. Razões entre fontes de coberturas diferentes recebem o rótulo de cobertura de jurisdição e ficam proibidas de operar como fator de correção.

O gasto previdenciário nunca é somado ao custo. O IPEA o calcula e o exclui da função de custo, com a justificativa expressa de que somá-lo à perda de produção implicaria dupla contagem, porque o benefício financia a perda de renda em vez de constituir perda adicional. O mesmo vale para o hospitalar e o pré-hospitalar, já embutidos no vetor M: eles se substituem, não se acrescentam.

## Situação de cada eixo, medida sobre os dados

| Eixo | Fonte candidata | Situação | Medição |
|---|---|---|---|
| 1 | RENAEST | parcial, com lacuna grande | 19,0% dos acidentes têm jurisdição e gravidade ao mesmo tempo |
| 2 | nenhuma | **sem fonte disponível** | ver adiante |
| 3 | SIH com valor | bloqueado até nova coleta | o dado monetário não existe localmente |

**Eixo 1.** O RENAEST tem 8.558.530 acidentes e 13.044.591 vítimas. O tipo de rodovia é útil em 32,2% dos registros, sendo 63,6% marcados como não informado. A gravidade da lesão é útil em 53,1%. A interseção, que é o que o produto escalar exige, cobre 19,0%, ou 1.628.736 acidentes: 1.230.359 municipais, 272.068 estaduais e 126.309 federais. O cálculo é possível, e o resultado será um piso de um piso, cuja lacuna de 81% precisa ser declarada com o mesmo destaque do número.

**Eixo 2.** Duas fontes foram avaliadas e as duas foram descartadas com medição.

O microdado do SIM não identifica a jurisdição da via. O dicionário oficial define o campo de local de ocorrência como tipo de lugar, com as categorias hospital, outro estabelecimento de saúde, domicílio, via pública, outros, aldeia indígena e ignorado. A categoria via pública engloba rodovia federal, estadual, municipal e rua urbana, sem distinguir. Não há coluna de rodovia, BR ou quilômetro no microdado.

O RENAEST é menos completo que a PRF na malha federal. Ele traz 126.309 acidentes federais utilizáveis, contra 473.646 ocorrências federais registradas pela PRF no mesmo período, o que dá 27%. Auditar a PRF com uma fonte que registra um quarto do que ela registra inverteria o sinal do resultado. E não há chave que ligue o identificador do RENAEST ao da PRF, o que impede distinguir acidente ausente de acidente não pareado.

A conclusão é que **a subnotificação da malha federal não é mensurável com os dados abertos hoje disponíveis**. Essa impossibilidade é ela mesma um achado, e sustenta um pedido de acesso à informação dirigido ao pareamento entre o registro policial e o registro de óbito.

**Eixo 3.** Os arquivos locais do SIH trazem apenas a contagem de internações. O valor da autorização, os dias de permanência e os dias de terapia intensiva exigem nova coleta no DATASUS, prevista para a preparação do artigo.

## Alternativas consideradas

**Tratar tudo como um intervalo entre piso e teto.** É a formulação intuitiva, e foi descartada porque somaria acidentes de jurisdições diferentes à omissão de registro de uma delas, e porque somaria ao valor do IPEA componentes que ele já embute. O resultado seria um intervalo largo cuja diferença não teria interpretação.

**Adotar um fator único de correção sobre o piso federal.** Foi o caminho da planilha V07, com os cenários de 1,0, 1,4 e 1,96. Descartado porque um fator único mistura os três eixos e esconde a origem de cada correção.

**Usar o RENAEST federal para medir a subnotificação da PRF.** Chegou a ser adotada e foi revogada pela medição, como registra o histórico de revisão abaixo.

**Calcular apenas a malha federal e declarar o restante fora de escopo.** Preservaria o rigor ao preço de responder metade da pergunta de política pública. Descartado.

## Consequências

Ganha-se a separação entre o que se sabe e o que não se sabe. O piso federal está medido, o eixo 1 é parcialmente alcançável com lacuna declarada, e o eixo 2 fica em aberto com a razão da impossibilidade registrada. Uma lacuna nomeada vale mais que um número inventado para preenchê-la.

Ganha-se a regra de recusa, já implementada em código: nenhuma razão entre fontes de cobertura distinta pode operar como fator de correção, e a função que devolve a cobertura de jurisdição levanta exceção quando pedida como fator de subnotificação.

Perde-se a possibilidade de anunciar um teto federal completo. Enquanto o eixo 2 não tiver fonte, o teto permanece parcial, e essa parcialidade é declarada em vez de coberta por analogia.

Assume-se a dívida da nova coleta do SIH com valor, e a de formular o pedido de acesso à informação sobre o pareamento entre registro policial e registro de óbito.

## Histórico de revisão

A primeira versão deste ADR, escrita hoje, afirmava que o microdado do SIM com local de ocorrência media o eixo 2. A leitura do dicionário oficial mostrou que o campo indica o tipo de lugar, e não a jurisdição da via.

A segunda versão substituiu o SIM pelo RENAEST federal como fonte do eixo 2. A contagem sobre a base completa mostrou que o RENAEST registra 27% do que a PRF registra na malha federal, o que o desqualifica como auditor dela.

As duas correções têm a mesma causa: a afirmação veio antes da medição. Fica a regra de que nenhuma fonte entra neste registro como capaz de medir um eixo antes de a sua cobertura ser contada sobre a base inteira, e não sobre amostra.

## Reversibilidade

Média. A decomposição organiza a apresentação dos resultados, não a estrutura do banco, e reverter significaria reescrever tabelas e legendas, sem migração de dado. O que não se reverte sem prejuízo é a regra de recusa: voltar a permitir razões entre coberturas distintas como fator de correção reintroduziria o defeito que este registro existe para impedir.
