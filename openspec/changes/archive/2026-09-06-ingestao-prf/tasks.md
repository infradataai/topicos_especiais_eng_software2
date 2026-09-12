# Tarefas — ingestão e normalização da PRF

Rastreabilidade: cada tarefa aponta o requisito da spec e o teste que a verifica.

## 1. Leitura por unidade da federação

- [x] 1.1 Ler o arquivo anual em blocos, como texto, e filtrar pela UF.
      Requisito: leitura por UF · Teste: `test_le_apenas_as_linhas_da_uf_pedida`
- [x] 1.2 Falhar de forma explícita quando faltar `pesid`, `id_veiculo` ou `id`.
      Requisito: caso de borda da chave ausente · Teste: `test_arquivo_sem_pesid_falha_em_vez_de_deduplicar_por_aproximacao`

## 2. Normalização por grão

- [x] 2.1 Separar ocorrências, veículos, pessoas e causas em tabelas próprias.
      Requisito: normalização em grão único · Teste: `test_deduplica_pessoas_e_veiculos_sem_perder_causas`
- [x] 2.2 Deduplicar cada tabela pela sua chave.
      Requisito: idem · Teste: idem
- [x] 2.3 Preservar causa e tipo no grão correto.
      Requisito: preservar causa e tipo · Teste: `test_preserva_causas_e_tipos_no_grao_proprio`

## 3. Reconhecimento de data

- [x] 3.1 Converter `AAAA-MM-DD` e `DD/MM/AAAA` por padrão próprio, sem inferência.
      Requisito: reconhecimento determinístico · Teste: `test_data_iso_e_brasileira_no_mesmo_pipeline`
- [x] 3.2 Garantir que dia acima de 12 no formato brasileiro não vire nulo.
      Requisito: caso de borda de 2022 · Teste: `test_dia_maior_que_doze_no_formato_brasileiro_nao_vira_nulo`
- [x] 3.3 Declarar como nulo apenas o que não casa com formato conhecido.
      Requisito: texto fora de formato · Teste: `test_texto_fora_de_formato_conhecido_vira_nulo_declarado`

## 4. Gravidade

- [x] 4.1 Mapear estado físico para as quatro categorias.
      Requisito: classificação explícita · Teste: `test_gravidade_mapeada_a_partir_do_estado_fisico`
- [x] 4.2 Tratar ausência como `nao_informado`.
      Requisito: estado físico não informado · Teste: `test_nao_informado_vira_categoria_e_nao_nulo`

## 5. Validação

- [x] 5.1 Conferir gravidade contra os indicadores do arquivo.
      Requisito: validação cruzada · Teste: `test_validacao_confirma_contagem_por_gravidade`
- [x] 5.2 Conferir unicidade das chaves e reconhecimento das datas.
      Requisito: idem · Teste: `test_validacao_acusa_chave_duplicada`

## 6. Vetor C

- [x] 6.1 Contar pessoas por gravidade e veículos por tipo, por ocorrência.
      Requisito: montagem do vetor C · Teste: `test_vetor_c_conta_pessoas_e_veiculos_por_ocorrencia`

## 7. Execução e evidência

- [x] 7.1 Rodar sobre o RN, de 2019 a 2025, e gravar as quatro tabelas.
- [x] 7.2 Gravar o relatório de ingestão por ano e o relatório de validação.
- [x] 7.3 Registrar a evidência numérica no documento de análise.

## 8. Pendente

- [ ] 8.1 Mapear os 24 tipos de veículo da PRF para as sete classes do IPEA.
- [ ] 8.2 Definir a regra de tratamento das pessoas com gravidade `nao_informado`.
- [ ] 8.3 Estender a execução às demais unidades da federação, para a escala nacional.
