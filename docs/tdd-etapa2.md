# Etapa 2 — TDD como guard-rail

## Ciclo Red-Green-Refactor (com evidência)

A funcionalidade escolhida foi a detecção de outliers pela regra do IQR (`src/analise.py::detectar_outliers_iqr`), útil ao validador de qualidade e ao requisito de detecção automática de outliers do projeto final.

**Red.** O teste foi escrito antes da implementação, em `tests/test_analise_outliers.py`, cobrindo cinco casos, inclusive bordas (lista vazia, lista curta, todos iguais). Rodado sem o módulo, falha:

```text
tests/test_analise_outliers.py:3: in <module>
    from src.analise import detectar_outliers_iqr
E   ModuleNotFoundError: No module named 'src.analise'
1 error in 0.19s
```

**Green.** A implementação mínima foi escrita para satisfazer o teste, e os cinco casos passam:

```text
tests/test_analise_outliers.py .....                    [100%]
5 passed in 0.10s
```

**Refactor.** Com o teste verde como guard-rail, a função foi mantida enxuta: guarda para menos de quatro pontos, guarda para IQR igual a zero, e regra de Tukey (k = 1,5). A suíte completa segue verde (21 testes).

A evidência de "teste antes da implementação" está no histórico de commits: o commit Red adiciona só o arquivo de teste (que falha); o commit Green adiciona o `src/analise.py` que o faz passar.

## Investigação da ferramenta de enforcement: TDD Guard

Investiguei o **TDD Guard** (github.com/nizos/tdd-guard), um hook para o Claude Code que automatiza o enforcement do ciclo. Ele roda a cada escrita de arquivo e usa um modelo "juiz" separado para verificar se o processo seguiu Red-Green-Refactor; se detecta implementação sem um teste falhando, bloqueia a escrita e explica o que falta. Requer Node.js 22+ e um framework de teste suportado, entre eles o pytest, que é o do projeto.

Como se comportaria no nosso cenário: na tarefa de outliers, ao tentar escrever `detectar_outliers_iqr` sem antes existir um teste falhando, o TDD Guard teria bloqueado a escrita com a mensagem de que nenhum teste falhando foi encontrado, forçando o Red primeiro. Na etapa Green, ele barraria implementação além do que o teste exige. É um enforcement que combina com o hook de permissão que já criamos na Etapa 1: um protege o dado, o outro protege o processo.

## Comparação: com TDD versus sem TDD

A segunda funcionalidade, `nivel_risco`, foi escrita de propósito **sem teste antes**, implementada direto. A diferença apareceu num caso de borda. A função classifica um trecho por faixa de taxa, mas aceita silenciosamente uma taxa negativa (entrada inválida) e a devolve como risco "baixo". Um teste posterior (`tests/test_analise_risco.py`, marcado `xfail`) documenta essa lacuna:

```text
tests/test_analise_risco.py ..x                         [100%]
21 passed, 1 xfailed
```

O contraste é direto. A função feita com TDD nasceu com as bordas cobertas (vazio, curto, todos iguais), porque escrever o teste primeiro obrigou a decidir cada caso antes de codificar. A função feita sem TDD resolveu o caminho feliz e deixou passar a validação de entrada, que só foi notada quando um teste foi escrito depois. Confirma a lição da aula: o teste primeiro define o que é "correto" e força o autor a enfrentar os casos de borda que o modelo, sozinho, tende a ignorar.
