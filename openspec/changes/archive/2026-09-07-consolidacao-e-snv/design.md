# Design — consolidação em SQLite e ancoragem no SNV

## Esquema

Sete tabelas, cada uma com o grão da sua origem:

    ocorrencias      id (PK), uf, br, km, data, ano, mes, classificacao, lat, lon
    veiculos         id, id_veiculo (PK composta), tipo_veiculo, classe_ipea
    pessoas          id, pesid (PK composta), gravidade, idade, sexo, tipo_envolvido
    causas_tipos     id, causa_acidente, tipo_acidente (PK composta)
    segmentos_snv    safra, codigo (PK composta), br, uf, km_inicial, km_final,
                     extensao, administracao, jurisdicao, tipo_trecho, regime
    custo_ocorrencia id (PK), total, subtotal_pessoas, subtotal_veiculos,
                     subtotal_institucional, categoria, base_monetaria
    ancoragem        id (PK), safra, codigo_segmento, houve_desempate, motivo

    proveniencia     tabela, orgao, arquivo, referencia, carregado_em

A tabela de ancoragem fica separada da de ocorrências porque a ancoragem depende da safra e pode ser refeita sem tocar no fato. A de proveniência é transversal e atende ao requisito de rastreamento.

## Idempotência

A carga usa a instrução de inserção que ignora conflito de chave primária, o que torna a repetição inofensiva sem exigir leitura prévia. A alternativa de apagar e recarregar a tabela foi descartada: ela perde a proveniência das cargas anteriores e transforma um erro de execução em perda de dado.

## Por que SQLite

O volume cabe: 473 mil ocorrências nacionais, com as tabelas derivadas, ficam na casa de centenas de megabytes. Não há concorrência de escrita, porque a carga é em lote e a leitura da aplicação é somente de consulta. E o servidor MCP de SQLite já está configurado no projeto, o que entrega a consulta em linguagem natural sem código novo. A troca por PostgreSQL fica registrada como caminho de escala, quando a cobertura nacional passar a receber escrita concorrente.

## Leitura do SNV

O cabeçalho da planilha está na terceira linha, e as duas primeiras trazem a versão da safra e o contato do DNIT. A leitura fixa essa posição e valida os rótulos esperados, em vez de procurar o cabeçalho, porque procurar aceitaria em silêncio uma planilha de formato diferente.

Os nomes de coluna vêm com espaços de sobra, como em `UF `, e são normalizados na leitura.

## Ancoragem e o problema dos coincidentes

O referenciamento é uma busca por intervalo: o segmento cuja faixa contém o quilômetro. O caso simples tem solução única. O caso dos trechos coincidentes, em que a mesma via física carrega mais de uma designação de rodovia, produz mais de um candidato: no Rio Grande do Norte há sete pares sobrepostos.

A regra de desempate prefere o eixo principal, depois o segmento de menor extensão e, por fim, o de menor código. A preferência pelo eixo principal segue a lógica do próprio SNV, que trata contornos, acessos e anéis como derivações. A menor extensão desempata porque o segmento mais curto é o mais específico, e o critério de código garante que a escolha seja determinística, e não dependente da ordem de leitura.

Cada desempate fica registrado na tabela de ancoragem. Isso permite medir quanto do resultado depende da regra, em vez de escondê-la.

## Regime de administração

A coluna `Administração` do SNV é a fonte do regime. Na safra de janeiro de 2025, `Federal` marca 4.801 segmentos, que são a malha do DNIT, e `Concessão Federal` marca 1.111, que são a malha da ANTT. As demais administrações, estaduais, municipais, distritais e de convênio, recebem o rótulo `outro` e ficam fora da comparação entre regimes, porque a base de sinistros da PRF cobre a malha federal.

A comparação entre regimes só é válida com o custo calculado pela composição de cada ocorrência, como o ADR-008 fixou. Comparar regimes usando uma média nacional faria a diferença observada refletir a frota de cada trecho, e não a administração da via.

## Rastreabilidade

Cada cenário das duas specs tem um teste correspondente, em `tests/test_persistencia.py` e `tests/test_snv.py`.
