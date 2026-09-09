# Proposta — Consolidação em banco relacional e ancoragem no SNV

## Por quê

O pipeline hoje termina em arquivos Parquet. Isso serve ao cálculo em lote e não serve a mais nada: não há consulta, não há API possível sobre ele, não há como o servidor MCP responder em linguagem natural, e a proveniência de cada carga vive num CSV solto. O requisito de consolidação em banco relacional único, declarado ao professor no checkpoint, continua aberto, e é ele que destrava a camada de aplicação inteira.

Falta também a etapa que dá endereço ao custo. O cálculo produz o custo de cada ocorrência, mas não sabe em que trecho da malha ela aconteceu. Sem a ancoragem no Sistema Nacional de Viação, não há mapa de trechos críticos, não há custo por quilômetro e não há comparação entre o trecho administrado pelo DNIT e o concedido à ANTT.

As duas mudanças entram juntas porque a ancoragem grava no banco, e separá-las obrigaria a escrever duas vezes a mesma camada de persistência.

## O que muda

Adiciona uma camada de persistência em SQLite, com esquema declarado por SQLAlchemy, que recebe as tabelas de grão único da ingestão, o custo por ocorrência e os segmentos do SNV. A carga é idempotente e cada linha carrega a sua proveniência: o órgão de origem, o arquivo, a safra e o instante da carga.

Adiciona o módulo de referenciamento linear, que lê as planilhas do SNV, seleciona a safra vigente no ano de cada sinistro e ancora a ocorrência ao segmento cuja faixa de quilometragem a contém. O segmento carrega o regime de administração, extraído da coluna própria do SNV, o que permite separar a malha do DNIT da malha concedida à ANTT.

## Fora de escopo

A API e a interface web, que consomem o banco e entram em mudança própria. A criticidade por exposição, que depende do VMDa. Os relatórios em JSON e PDF. A ingestão do DATASUS e do PNCT, previstas na sequência, cada uma com a sua spec.

## O que a leitura do SNV revelou

A planilha traz o cabeçalho na terceira linha, e não na primeira. A coluna `Administração` distingue os regimes: na safra de janeiro de 2025 há 4.801 segmentos federais sob o DNIT e 1.111 sob concessão federal, que é a malha da ANTT. A coluna `Jurisdição` separa a malha federal das estaduais e municipais coincidentes, que a planilha também lista.

O Rio Grande do Norte tem 207 segmentos em nove rodovias, somando 1.896,6 km com todas as jurisdições. Sete pares desses segmentos se sobrepõem em quilometragem, o que caracteriza os trechos coincidentes, em que a mesma via física recebe mais de uma designação de rodovia. A ancoragem precisa de uma regra de desempate para esses casos, sob pena de a mesma ocorrência ser contada em dois segmentos.
