# Tarefas - Geometria oficial do SNV

Rastreabilidade: cada tarefa aponta o requisito da spec e o teste que a verifica.
O teste vem antes da implementacao.

## 1. Esquema

- [x] 1.1 Acrescentar a tabela `geometria_segmento` ao esquema, com codigo, safra e pontos.

## 2. Ingestao

- [x] 2.1 Escrever o teste da leitura de um shapefile pequeno, filtrando a UF.
      Requisito: ingestao da geometria · Teste: `test_ingere_geometria_de_shapefile`
- [x] 2.2 Escrever o teste da simplificacao, que reduz os pontos e preserva os extremos.
      Requisito: simplificacao · Teste: `test_simplifica_e_preserva_extremos`
- [x] 2.3 Implementar `scripts/ingerir_geometria_snv.py`, com funcao importavel e CLI.

## 3. Consulta

- [x] 3.1 Escrever o teste da preferencia pela geometria oficial.
      Requisito: tracado oficial · Teste: `test_prefere_geometria_oficial`
- [x] 3.2 Escrever o teste do recuo para a aproximacao.
      Requisito: recuo · Teste: `test_recua_para_aproximacao_sem_geometria`
- [x] 3.3 Ler a geometria oficial em `geometria_segmentos`, com recuo por sinistros.

## 4. Execucao

- [x] 4.1 Ingerir a safra 202507A do Rio Grande do Norte no banco.
- [x] 4.2 Medir a cobertura da geometria sobre os 171 segmentos.
- [x] 4.3 Conferir o tracado no mapa.
