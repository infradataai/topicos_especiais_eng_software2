# Tarefas - Mapa dos trechos críticos

Rastreabilidade: cada tarefa aponta o requisito da spec e o teste que a verifica.
O teste vem antes da implementação.

## 1. Consultas do esquema de sinistros

- [x] 1.1 Escrever o teste do ranque de segmentos nas duas leituras.
      Requisito: consulta de segmentos · Teste: `test_segmentos_traz_as_duas_leituras`
- [x] 1.2 Escrever o teste da junção por código e safra.
      Requisito: consulta de segmentos · Teste: `test_nao_multiplica_custo_por_safra`
- [x] 1.3 Escrever o teste do segmento sem exposição.
      Requisito: caso de borda · Teste: `test_segmento_sem_vmda_tem_leitura_por_exposicao_nula`
- [x] 1.4 Implementar `custo_social_core/consultas.py`.

## 2. Rotas da aplicação

- [x] 2.1 Escrever o teste da rota de segmentos.
      Requisito: rota de segmentos · Teste: `test_rota_segmentos_responde_ordenada`
- [x] 2.2 Escrever o teste da rota de ocorrências com coordenada.
      Requisito: rota de ocorrências · Teste: `test_rota_ocorrencias_traz_coordenada_e_custo`
- [x] 2.3 Escrever o teste do banco sem as tabelas do núcleo.
      Requisito: caso de borda · Teste: `test_banco_sem_tabelas_de_sinistro_recusa_com_mensagem`
- [x] 2.4 Escrever o teste da ordenação fora da lista permitida.
      Requisito: caso de borda · Teste: `test_ordenacao_nao_permitida_e_recusada`
- [x] 2.5 Implementar as rotas em `src/consulta_web.py`.

## 3. Página do mapa

- [x] 3.1 Escrever o teste da página do mapa.
      Requisito: página do mapa · Teste: `test_pagina_do_mapa_responde_html`
- [x] 3.2 Implementar a página.
