# Tarefas — cálculo do custo social por ocorrência

Rastreabilidade: cada tarefa aponta o requisito da spec e o teste que a verifica.
As tarefas seguem a ordem do TDD: o teste vem antes da implementação.

## 1. Vetor M como configuração

- [x] 1.1 Declarar as três subtabelas da Tabela 1 do TD 2565, a preços de dezembro de 2014,
      indexadas por componente e gravidade da ocorrência.
      Requisito: seleção da coluna do vetor M
- [x] 1.2 Declarar o deflator 1,884802 e a base de junho de 2026.
      Requisito: atualização monetária com base única
- [x] 1.3 Declarar a tabela de mapeamento dos tipos da PRF para as sete classes do IPEA.
      Requisito: custo associado aos veículos

## 2. Seleção da coluna

- [x] 2.1 Escrever o teste da mesma vítima em ocorrências de gravidade diferente.
      Requisito: seleção da coluna · Teste: `test_mesma_vitima_custa_diferente_conforme_a_ocorrencia`
- [x] 2.2 Escrever o teste da classificação desconhecida.
      Requisito: caso de borda · Teste: `test_classificacao_desconhecida_falha`
- [x] 2.3 Implementar a seleção.

## 3. Custo das pessoas

- [x] 3.1 Escrever o teste da soma de gravidades distintas.
      Requisito: custo das pessoas · Teste: `test_soma_pessoas_de_gravidades_distintas`
- [x] 3.2 Escrever o teste da gravidade não informada com custo zero e contagem declarada.
      Requisito: gravidade não informada · Teste: `test_gravidade_nao_informada_nao_soma_e_e_declarada`
- [x] 3.3 Implementar `custo_pessoas`.

## 4. Regra de composição

- [x] 4.1 Escrever o teste do cavalo mecânico com semirreboque.
      Requisito: contagem de caminhões · Teste: `test_cavalo_com_semirreboque_conta_um_caminhao`
- [x] 4.2 Escrever o teste do bitrem.
      Requisito: caso de borda · Teste: `test_bitrem_conta_um_caminhao`
- [x] 4.3 Escrever o teste da carreta órfã.
      Requisito: caso de borda · Teste: `test_carreta_sem_tratora_conta_um_caminhao`
- [x] 4.4 Implementar `contar_caminhoes`.

## 5. Custo dos veículos

- [x] 5.1 Escrever o teste da motoneta valorada como motocicleta.
      Requisito: custo dos veículos · Teste: `test_motoneta_vale_como_motocicleta`
- [x] 5.2 Escrever o teste do tipo não mapeado.
      Requisito: caso de borda · Teste: `test_tipo_de_veiculo_nao_mapeado_falha`
- [x] 5.3 Implementar `custo_veiculos`.

## 6. Custo institucional

- [x] 6.1 Escrever o teste da ocorrência sem veículo registrado.
      Requisito: custo institucional · Teste: `test_ocorrencia_sem_veiculo_tem_so_o_institucional`
- [x] 6.2 Implementar `custo_institucional`.

## 7. Atualização monetária e regressão

- [x] 7.1 Escrever o teste que reproduz o exemplo trabalhado da memória de cálculo.
      Requisito: atualização monetária · Teste: `test_exemplo_trabalhado_ocorrencia_182341`
- [x] 7.2 Escrever o teste que confere o deflator contra a planilha V07.
      Requisito: atualização monetária · Teste: `test_deflator_reproduz_parametro_da_v07`
- [x] 7.3 Implementar `custo_ocorrencia`, com o deflator aplicado ao total.

## 8. Saída por categoria

- [x] 8.1 Escrever o teste da classificação pela vítima mais grave.
      Requisito: saída decomposta · Teste: `test_ocorrencia_classificada_pela_vitima_mais_grave`
- [x] 8.2 Implementar as duas leituras, por vítima e por ocorrência.

## 9. Execução e evidência

- [x] 9.1 Rodar sobre as 10.029 ocorrências do Rio Grande do Norte.
- [x] 9.2 Conferir o total contra os R$ 2,30 bilhões da planilha V07.
- [x] 9.3 Registrar o resultado e a conferência no documento de análise.

## 10. Pendente para depois

- [ ] 10.1 Variante observada: substituir o componente hospitalar pelo valor do SIH.
- [ ] 10.2 Variante atuarial: recalcular a perda de produção do óbito pela idade da vítima.
- [ ] 10.3 Sensibilidade: imputar a gravidade não informada pela distribuição da UF.
