# Tarefas - Faixa de dominio

Rastreabilidade: cada tarefa aponta o requisito da spec e o teste que a verifica.
O teste vem antes da implementacao.

## 1. Esquema

- [x] 1.1 Acrescentar a tabela `qualidade_geo` ao esquema.

## 2. Marcacao

- [x] 2.1 Escrever o teste da distancia ao eixo e do indicador de dentro da faixa.
      Requisito: marcacao · Teste: `test_marca_dentro_e_fora_da_faixa`
- [x] 2.2 Implementar `scripts/marcar_faixa_dominio.py`, com funcao importavel e CLI.

## 3. Consulta

- [x] 3.1 Escrever o teste do filtro do mapa pela faixa.
      Requisito: filtro · Teste: `test_mapa_filtra_pela_faixa`
- [x] 3.2 Escrever o teste do recuo sem a marca calculada.
      Requisito: recuo · Teste: `test_mapa_sem_marca_mostra_todos`
- [x] 3.3 Filtrar `ocorrencias_geo` pela faixa quando a marca existir.

## 4. Execucao

- [x] 4.1 Marcar os sinistros do Rio Grande do Norte, faixa de 50 metros.
- [x] 4.2 Medir quantos ficaram fora e conferir que o custo nao mudou.
