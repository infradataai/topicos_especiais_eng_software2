# Comparativo de prompts — prompt fraco x prompt eficaz

Atividade Assíncrona 1, Etapa 4. Disciplina Tópicos Avançados em Engenharia de Software 2, PPgTI/UFRN-IMD.

## Funcionalidade escolhida

Uma função que lê a coluna de datas do CSV da PRF e a converte para `datetime` de forma determinística. A escolha vem de um problema real do pipeline: o CSV da PRF de 2022 traz datas no formato dia/mês, e o processamento dependente do ambiente produz contagens diferentes entre máquinas. O registro de decisão ADR-026 fixa `dayfirst=True` para eliminar essa não-determinância. A função vive em `src/parse_datas.py` e tem teste em `tests/test_parse_datas.py`.

## Modelos usados

O prompt eficaz foi executado com um modelo de maior capacidade (Claude Opus). O mesmo par de prompts foi repetido com um modelo de menor capacidade (Claude Haiku), para observar o efeito da capacidade do modelo sobre a qualidade da resposta. As respostas abaixo são representativas do que cada configuração produz.

## Prompt fraco

> Faça uma função em Python que converte datas.

Resposta representativa:

```python
import pandas as pd

def converter_datas(df, coluna):
    df[coluna] = pd.to_datetime(df[coluna])
    return df
```

O código roda, mas ignora o problema central. Sem `dayfirst=True`, o pandas infere o formato pela ordem dos valores e pelo ambiente, o que faz "03/02/2022" virar 2 de março em uma máquina e 3 de fevereiro em outra. Não trata valores inválidos, o que interrompe a execução em qualquer célula malformada. E altera o DataFrame recebido no lugar, efeito colateral que dificulta o teste.

## Prompt eficaz

> Contexto: no projeto do pipeline de sinistros (Python, pandas), preciso de uma função em `src/parse_datas.py` que converta a coluna de datas do CSV da PRF, hoje lida como texto (dtype str), no formato DD/MM/AAAA.
> Padrão a seguir: o projeto exige leitura determinística de datas, conforme o ADR-026, que fixa `dayfirst=True`; siga essa convenção.
> Restrições: não adicione dependências além de pandas; não altere o objeto recebido no lugar; marque valores inválidos como `NaT` em vez de lançar exceção; inclua docstring com entrada e saída.
> Validação: a função deve passar em um teste pytest que verifique a interpretação dia-primeiro e o tratamento de valor inválido.

Resposta:

```python
from __future__ import annotations

import pandas as pd


def parse_data_prf(serie: pd.Series) -> pd.Series:
    """Converte uma coluna de datas da PRF para datetime de forma deterministica.

    Le sempre com dayfirst=True (dia primeiro), independentemente do locale da
    maquina, e marca valores invalidos como NaT em vez de lancar excecao.

    Args:
        serie: coluna de datas como texto (dtype str), no formato DD/MM/AAAA.

    Returns:
        Serie datetime64[ns]; entradas invalidas viram NaT.
    """
    return pd.to_datetime(serie, dayfirst=True, errors="coerce")
```

Este código respeita a convenção do projeto, é determinístico entre máquinas, não tem efeito colateral e passa nos três testes de `tests/test_parse_datas.py`.

## Comparação

A diferença central está no determinismo, que o prompt fraco ignora e o eficaz garante ao fixar `dayfirst=True`, exatamente o ponto que o ADR-026 protege. O prompt eficaz também produziu tratamento de erro com `NaT`, ausência de efeito colateral e docstring, porque as restrições foram declaradas. O prompt fraco entregou código que roda, mas que introduziria um viés silencioso na série temporal e quebraria diante de dados sujos. Em síntese, a qualidade do resultado seguiu a qualidade do contexto e das restrições fornecidas, e não a capacidade bruta do modelo.

## Repetição com modelo de menor capacidade

Com o modelo de menor capacidade, o prompt fraco gerou um código igualmente genérico, sem `dayfirst`. O prompt eficaz, com as mesmas quatro instruções, também levou o modelo menor a incluir `dayfirst=True` e o `errors="coerce"`, embora com docstring mais curta e sem as anotações de tipo. A lição se confirma: um contexto bem escrito recupera boa parte da diferença entre os modelos, e a especificação clara importa mais do que a escolha do modelo para uma tarefa pequena e bem delimitada.
