# ADR-011 — Parâmetros do cálculo de custo social: base monetária, gravidade ausente e mapeamento de veículos

Formato MADR. Numeração própria da sandbox da disciplina.

- Status: ACEITO
- Data: 2026-09-07
- Decisores: Flávio Eduardo Batista Moreira e Bruno dos Santos Fernandes da Silva
- Relaciona-se com: ADR-009 (ingestão determinística da PRF)
- Memória de cálculo: `docs/memoria-calculo-CM.md`

## Contexto

O custo social de cada ocorrência é o produto escalar entre o vetor C, que conta pessoas por gravidade e veículos por classe, e o vetor M de custos médios padrão da Tabela 1 do Texto para Discussão 2565 do IPEA, a preços de dezembro de 2014. Três parâmetros precisam ser fixados antes de o cálculo rodar, e os três governam o mesmo resultado, razão de estarem num só registro.

## Decisão 1 — Base monetária de junho de 2026

Os valores da Tabela 1 são trazidos de dezembro de 2014 para junho de 2026 pelo IPCA acumulado, com fator 1,884802. A multiplicação ocorre ao final, sobre o total da ocorrência, e não componente a componente.

A conferência fecha com a planilha V07, que já adota essa base: 23.498,77 × 1,884802 = 44.290,53, o custo do acidente sem vítimas.

**Alternativas.** Adotar a data corrente de execução tornaria o resultado móvel a cada rodada e impediria a comparação entre versões. Manter dezembro de 2014 preservaria a fonte, ao custo de um número sem leitura prática. As duas foram descartadas.

## Decisão 2 — Gravidade não informada com custo zero e total declarado

As pessoas cujo estado físico não consta entram no cálculo com custo zero, e a sua contagem é publicada ao lado do resultado. São 1.703 pessoas no Rio Grande do Norte, ou 7,2% do total. A imputação da gravidade pela distribuição observada da própria unidade da federação fica registrada como análise de sensibilidade, e não como cálculo principal.

**Alternativas.** Excluir essas pessoas da base esconderia a lacuna e impediria medir a completude. Imputar no cálculo principal produziria um total mais completo e menos verificável, com a imputação embutida no número que a banca lê. A leitura transparente foi preferida à leitura completa.

## Decisão 3 — Mapeamento dos tipos de veículo e regra de composição

Os vinte e dois tipos registrados pela PRF no Rio Grande do Norte são mapeados para as sete classes do IPEA da seguinte forma. Automóvel vai para Automóveis. Motocicleta, motoneta, ciclomotor, triciclo e quadriciclo vão para Motocicletas. Bicicleta vai para Bicicletas. Caminhonete, camioneta e utilitário vão para Utilitários. Caminhão e caminhão-trator vão para Caminhões. Ônibus e micro-ônibus vão para Ônibus. Carroça-charrete, trator de rodas, motor-casa, carro de mão, trem-bonde e a própria categoria outros vão para Outros.

O semirreboque e o reboque não recebem valor próprio. Eles integram a composição da unidade tratora, e a contagem de caminhões por ocorrência segue a regra: o número de tratoras, quando houver ao menos uma; um caminhão, quando houver carreta e nenhuma tratora; zero nos demais casos.

Três apoios sustentam a regra. A decomposição do IPEA de 2006 tem sete classes de veículo e nenhuma de reboque, o que indica que a carreta não foi unidade amostral. A PRF conta por identificador de veículo, que é unidade de licenciamento, enquanto o vetor M foi calibrado na unidade econômica de reparo. E o dado confirma o pareamento: das 477 ocorrências com carreta, 420 têm a tratora na mesma ocorrência.

**Alternativas medidas.** As quatro regras possíveis foram calculadas sobre a classe Caminhões do Rio Grande do Norte, a preços de junho de 2026.

| Regra | Unidades | Custo da classe (R$) |
|---|---:|---:|
| Carreta nunca conta | 1.410 | 140.079.515,34 |
| **Adotada: composição uma vez; carreta órfã vale um caminhão** | **1.467** | **146.114.628,54** |
| Toda carreta excedente conta | 1.573 | 156.421.385,45 |
| Tratora e carreta contam separadamente | 2.024 | 200.556.347,82 |

A primeira foi descartada porque apagaria o caminhão das 57 ocorrências em que só a carreta foi registrada, acidentes que envolveram 66 automóveis e 44 motocicletas. A terceira foi descartada porque contaria duas vezes as 91 ocorrências de bitrem e rodotrem, em que uma tratora puxa duas carretas. A quarta, que era a leitura literal do mapeamento inicial, foi descartada por cobrar duas vezes o dano da mesma composição, com efeito de R$ 60,5 milhões, ou 14,8% do custo de veículos do estado.

Tratar o semirreboque como Outros também foi considerado e descartado. A classe Outros custa R$ 79.931,58 no acidente com vítimas, mais que o próprio caminhão, e usá-la para a carreta classificaria por conveniência de valor, e não por natureza do veículo.

## Consequências

Ganha-se um cálculo comparável com a planilha V07 e com a Tabela 3 do TD 2565, uma lacuna de gravidade que fica visível em vez de embutida, e um custo de veículos livre da dupla contagem da composição rodoviária.

Perde-se cobertura no total: as 1.703 pessoas sem gravidade não somam custo, e o resultado é, nesse ponto, um piso. A regra de composição introduz uma condicional por ocorrência, que precisa de teste próprio, sob pena de a contagem de caminhões voltar a divergir.

Assume-se a dívida de estender a verificação do mapeamento às demais unidades da federação, porque a distribuição de tipos de veículo varia entre estados e pode revelar tipos que o Rio Grande do Norte não registrou.

## Reversibilidade

Alta. Os três parâmetros são declarados em configuração, não embutidos na lógica, e mudar qualquer um deles significa alterar uma constante e reexecutar o cálculo, sem migração de dado. O deflator, o tratamento da gravidade ausente e a tabela de mapeamento ficam explícitos e versionados.
