# Tarefas — consolidação em SQLite e ancoragem no SNV

Rastreabilidade: cada tarefa aponta o requisito da spec e o teste que a verifica.
O teste vem antes da implementação.

## 1. Esquema relacional

- [x] 1.1 Declarar as sete tabelas e a de proveniência com SQLAlchemy.
      Requisito: esquema relacional único
- [x] 1.2 Escrever o teste da criação do esquema num banco novo.
      Teste: `test_cria_esquema_em_banco_novo`
- [x] 1.3 Implementar a criação do esquema.

## 2. Carga idempotente

- [x] 2.1 Escrever o teste da recarga da mesma origem.
      Requisito: carga idempotente · Teste: `test_recarregar_mesma_origem_nao_duplica`
- [x] 2.2 Escrever o teste da carga parcialmente nova.
      Teste: `test_carga_parcial_insere_so_o_inedito`
- [x] 2.3 Implementar a carga com inserção que ignora conflito de chave.

## 3. Proveniência

- [x] 3.1 Escrever o teste da consulta de proveniência de uma carga.
      Requisito: rastreamento de origem · Teste: `test_proveniencia_registra_orgao_arquivo_e_ano`
- [x] 3.2 Escrever o teste de duas origens na mesma tabela.
      Teste: `test_duas_origens_na_mesma_tabela`
- [x] 3.3 Implementar o registro de proveniência.

## 4. Consulta por UF

- [x] 4.1 Escrever o teste do custo por segmento filtrado por UF.
      Requisito: consulta por UF · Teste: `test_consulta_custo_por_segmento_de_uma_uf`
- [x] 4.2 Implementar as consultas.
- [x] 4.3 Escrever o teste do caminho do banco na pasta de dados.
      Requisito: nenhum dado pessoal versionado · Teste: `test_banco_fica_na_pasta_de_dados`

## 5. Leitura do SNV

- [x] 5.1 Escrever o teste da leitura de uma safra com filtro por UF.
      Requisito: leitura da planilha · Teste: `test_le_safra_e_filtra_uf`
- [x] 5.2 Escrever o teste do cabeçalho não reconhecido.
      Requisito: caso de borda · Teste: `test_cabecalho_inesperado_falha`
- [x] 5.3 Implementar a leitura, com cabeçalho na terceira linha e nomes normalizados.

## 6. Safra vigente

- [x] 6.1 Escrever o teste da safra vigente no ano do sinistro.
      Requisito: seleção da safra · Teste: `test_safra_vigente_no_ano_do_sinistro`
- [x] 6.2 Escrever o teste do sinistro anterior à primeira safra.
      Requisito: caso de borda · Teste: `test_sinistro_anterior_a_primeira_safra_falha`
- [x] 6.3 Implementar a seleção da safra.

## 7. Ancoragem

- [x] 7.1 Escrever o teste do quilômetro dentro da faixa.
      Requisito: ancoragem · Teste: `test_ancora_km_dentro_da_faixa`
- [x] 7.2 Escrever o teste do quilômetro fora de qualquer faixa.
      Requisito: caso de borda · Teste: `test_km_fora_da_faixa_nao_ancora_e_registra_motivo`
- [x] 7.3 Implementar a ancoragem.

## 8. Trechos coincidentes

- [x] 8.1 Escrever o teste do desempate entre segmentos sobrepostos.
      Requisito: desempate · Teste: `test_desempate_entre_segmentos_coincidentes`
- [x] 8.2 Implementar a regra: jurisdição federal, eixo principal, menor extensão, menor código.

## 9. Regime de administração

- [x] 9.1 Escrever os testes dos três casos de regime.
      Requisito: regime · Testes: `test_administracao_federal_e_dnit`,
      `test_concessao_federal_e_antt`, `test_administracao_estadual_e_outro`
- [x] 9.2 Implementar a derivação do regime.

## 10. Agregação por segmento

- [x] 10.1 Escrever o teste da soma de duas ocorrências no mesmo segmento.
      Requisito: agregação · Teste: `test_agrega_custo_por_segmento_e_por_km`
- [x] 10.2 Implementar a agregação.

## 11. Execução e evidência

- [x] 11.1 Carregar o banco do Rio Grande do Norte com as tabelas, o custo e os segmentos.
- [x] 11.2 Ancorar as 10.029 ocorrências e medir a taxa de ancoragem.
- [x] 11.3 Conferir a extensão da malha ancorada contra os 1.648,7 km da planilha V07.
- [x] 11.4 Produzir o ranque de trechos críticos por custo e por custo por quilômetro.
- [x] 11.5 Registrar os achados no documento de análise.

## 12. Pendente para depois

- [ ] 12.1 Comparação entre os regimes DNIT e ANTT, com o custo por quilômetro de cada um.
- [ ] 12.2 Ingestão do PNCT/VMDa, com spec própria.
- [ ] 12.3 Ingestão do DATASUS, com spec própria.
