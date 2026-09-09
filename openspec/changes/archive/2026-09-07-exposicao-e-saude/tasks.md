# Tarefas — exposição de tráfego (VMDa) e dados de saúde (DATASUS)

Rastreabilidade: cada tarefa aponta o requisito da spec e o teste que a verifica.
O teste vem antes da implementação.

## 1. Leitura do VMDa

- [x] 1.1 Escrever o teste da aba de dados com nome variável.
      Requisito: leitura do VMDa · Teste: `test_reconhece_aba_de_dados_por_conteudo`
- [x] 1.2 Escrever o teste do arquivo sem aba de dados.
      Requisito: caso de borda · Teste: `test_arquivo_sem_aba_de_dados_falha`
- [x] 1.3 Implementar a leitura, com a aba identificada por conteúdo.

## 2. Volume nos dois sentidos

- [x] 2.1 Escrever o teste dos dois sentidos preenchidos.
      Requisito: volume nos dois sentidos · Teste: `test_soma_os_dois_sentidos`
- [x] 2.2 Escrever o teste do sentido ausente.
      Requisito: caso de borda · Teste: `test_um_sentido_ausente_usa_o_presente_e_declara`
- [x] 2.3 Escrever o teste do segmento sem medição.
      Requisito: caso de borda · Teste: `test_sem_medicao_devolve_nulo_declarado`
- [x] 2.4 Implementar o cálculo do volume total.

## 3. Agregação de postos

- [x] 3.1 Escrever o teste do segmento com dois postos.
      Requisito: agregação de postos · Teste: `test_agrega_postos_pela_media_e_conta_quantos`
- [x] 3.2 Implementar a agregação pela média, com o número de postos registrado.

## 4. Exposição e criticidade

- [x] 4.1 Escrever o teste da exposição anual em veículos-quilômetro.
      Requisito: exposição anual · Teste: `test_exposicao_anual_em_veiculos_km`
- [x] 4.2 Escrever o teste do trecho movimentado contra o vazio.
      Requisito: criticidade · Teste: `test_trecho_vazio_tem_criticidade_maior`
- [x] 4.3 Escrever o teste do segmento sem exposição conhecida.
      Requisito: caso de borda · Teste: `test_sem_exposicao_nao_sai_do_ranque_por_km`
- [x] 4.4 Implementar a exposição e a criticidade.

## 5. Leitura do DATASUS

- [x] 5.1 Escrever o teste da marca de ordem de byte no cabeçalho.
      Requisito: leitura dos agregados · Teste: `test_le_csv_com_marca_de_ordem_de_byte`
- [x] 5.2 Implementar a leitura.

## 6. Óbitos e internações

- [x] 6.1 Escrever o teste da consulta de óbitos de uma UF num ano.
      Requisito: óbitos por transporte · Teste: `test_obitos_por_uf_e_ano`
- [x] 6.2 Escrever o teste da soma das internações do ano.
      Requisito: internações · Teste: `test_soma_internacoes_do_ano`
- [x] 6.3 Implementar as consultas.

## 7. Cobertura de jurisdição

- [x] 7.1 Escrever o teste do cálculo da cobertura.
      Requisito: cobertura · Teste: `test_calcula_cobertura_de_jurisdicao`
- [x] 7.2 Escrever o teste da recusa de uso como subregistro.
      Requisito: caso de borda · Teste: `test_recusa_usar_cobertura_como_subregistro`
- [x] 7.3 Implementar, com o rótulo explícito e a recusa.

## 8. Persistência

- [x] 8.1 Acrescentar as tabelas `exposicao_segmento`, `obitos_sim` e `internacoes_sih`
      ao esquema, com proveniência.
- [x] 8.2 Estender a consulta de custo por segmento com a exposição e a criticidade.

## 9. Execução e evidência

- [x] 9.1 Carregar o VMDa e os agregados do DATASUS no banco do Rio Grande do Norte.
- [x] 9.2 Medir a cobertura do VMDa sobre os segmentos com ocorrência.
- [x] 9.3 Produzir o ranque de trechos críticos nas duas leituras, por quilômetro e por exposição.
- [x] 9.4 Comparar os dois ranques e registrar a diferença como achado.

## 10. Pendente para depois

- [ ] 10.1 Substituir o componente hospitalar do vetor M pelo valor observado do SIH.
- [ ] 10.2 Custo do atendimento pré-hospitalar do SAMU.
- [ ] 10.3 Fator de subregistro com origem própria, distinta da cobertura de jurisdição.
