**Universidade Federal do Rio Grande do Norte**
**Instituto Metrópole Digital**
**Programa de Pós-Graduação em Tecnologia da Informação**
**Disciplina:** Tópicos Avançados em Engenharia de Software 2 (Desenv. de Software com IA)
**Professor:** Jean Mário Moreira de Lima
**Alunos:** Flávio Eduardo Batista Moreira e Bruno dos Santos Fernandes da Silva

# Reconstrução da base do RN e auditoria da planilha V07

---

## 1. O que foi feito

A base de sinistros do RN foi reconstruída a partir dos sete arquivos anuais nacionais da PRF, de 2019 a 2025, com as chaves `pesid` e `id_veiculo`. O arquivo bruto reúne 51.309 linhas do RN, que a normalização separa em quatro tabelas de grão único: 10.029 ocorrências, 18.016 veículos, 23.610 pessoas e 20.233 pares de causa e tipo. A redução por ano vai de 40,2% em 2019 a 58,8% em 2024, e nenhuma informação se perde, porque a causa e o tipo migram para a tabela própria em vez de serem descartados.

O módulo `ingestao_prf` e o script `reconstruir_prf` ficam no repositório público, e as tabelas em Parquet e CSV ficam na pasta de dados do repositório privado. Onze testes cobrem a deduplicação, o parsing de data, a validação e a montagem do vetor C.

## 2. Dois defeitos encontrados nos dados

O primeiro defeito estava no extrato antigo `uf_RN.csv`. Ele vem do conjunto "todas as causas e tipos" sem deduplicação e sem as chaves de pessoa e veículo. Contar as vítimas linha a linha nesse arquivo dá 1.570 óbitos onde há 547 no mesmo período, uma inflação de 187%. Os feridos graves inflam 122% e os leves 123%. O extrato também parava em 2024.

O segundo defeito estava no arquivo nacional de 2022, e afeta qualquer leitura da série. A coluna `data_inversa` vem em `DD/MM/AAAA` nesse ano e em `AAAA-MM-DD` em todos os outros. Com inferência automática de formato, as datas cujo dia passa de 12 viram nulo, e as demais têm dia e mês trocados. O efeito medido foi a perda de 791 das 1.288 ocorrências de 2022, exatamente a fração 12/31 que a regra prevê. A correção reconhece cada formato pelo seu próprio padrão, sem inferência, e recuperou os 100% das datas. O caso está travado por dois testes.

## 3. A base reconstruída

| Grão | Registros | Observação |
|---|---|---|
| Ocorrências | 10.029 | 1.561 sem vítimas, 7.820 com feridos, 648 fatais |
| Veículos | 18.016 | 24 tipos, a mapear para as sete classes do IPEA |
| Pessoas | 23.610 | 9.195 ilesos, 8.509 leves, 3.034 graves, 713 óbitos |
| Causas e tipos | 20.233 | preservados no grão correto |

A validação cruzada confirma a deduplicação: a contagem de pessoas por gravidade bate exatamente com a soma dos indicadores do próprio arquivo, nas quatro categorias. As chaves são únicas nos três grãos. Restam 1.703 pessoas com estado físico "Não Informado" e 456 com o campo vazio, que somam 9,1% e ficam declaradas como categoria própria, sem virar nulo silencioso.

## 4. Auditoria da planilha V07

A V07 resiste bem à conferência no nível em que opera. As contagens do RN divergem em 0,3% da base reconstruída (9.997 contra 10.029 ocorrências), o que mostra que ela não usou o extrato inflado. O custo do RN recalculado com os parâmetros dela dá R$ 2,307 bilhões contra os R$ 2,302 bilhões registrados, uma diferença de 0,2%. As notas metodológicas de cada aba são explícitas quanto às próprias ressalvas, e a aba de custo por vida se declara sensibilidade e não revaloração.

Três pontos pedem correção.

**O grão limita o resultado.** A V07 valora por ocorrência, nas três classes do TD 2565. As quatro categorias por vítima que o projeto busca exigem o vetor C do modelo aditivo, que agora existe. É o aperfeiçoamento principal, e ele não corrige um erro da planilha: amplia a granularidade dela.

**O teto de subregistro mede outra coisa.** A aba declara "Teto 1,96 = SIM total/via pública". Para o RN, os 475 óbitos de transporte de 2019 contra os 241 em via pública dão exatamente 1,97. Essa razão compara o total de óbitos por transporte com a parcela que ocorreu na via, e reflete que a maior parte das vítimas morre depois, no hospital. Ela não mede o quanto a PRF deixa de registrar. Usá-la como teto de subregistro troca o objeto medido. A medição correta compara os óbitos da PRF com os óbitos do SIM ocorridos em rodovia federal, o que exige o local de ocorrência do SIM.

**O fator central não tem âncora no RN.** O central de 1,4 vem da razão entre o SIM e o RENAEST. A própria aba de completude registra que o RENAEST não preenche a gravidade no RN, no MA, no AP e no PA, e nesses estados o registro de óbito é zero. O fator nacional, portanto, é estimado onde o RENAEST funciona e aplicado ao piloto onde ele não funciona. Para o RN, a correção precisa de outro lastro.

A conferência de cobertura reforça o ponto. Os óbitos da PRF no RN correspondem a 21,9% dos óbitos de transporte do SIM no estado, com estabilidade entre 18,9% e 23,5% ao longo dos sete anos. Essa fração mede jurisdição, porque a PRF cobre a rodovia federal e o SIM cobre todas as vias. Confundir jurisdição com subregistro inflaria o custo federal em quatro vezes e meia.

## 5. Correções propostas para a planilha

A primeira correção substitui o teto de 1,96 por uma faixa ancorada em subregistro de fato. Enquanto o local de ocorrência do SIM não estiver processado, a faixa da literatura de morte tardia, de 1,1 a 1,3, é mais defensável que a razão atual, e a aba registra a troca de âncora.

A segunda correção separa jurisdição de subregistro em duas linhas distintas do memorial, para que a fração federal de 21,9% nunca seja lida como falha de registro.

A terceira correção acrescenta a coluna de grão à aba de parâmetros, declarando que o custo é por ocorrência, e reserva o espaço da valoração por vítima que o vetor C passa a permitir.

A quarta correção troca o extrato de origem do RN pela base reconstruída, e passa a incluir 2025.

## 6. Próximo passo

Com a base reconstruída e o vetor C montados, o passo seguinte é aplicar o vetor M da Tabela 1 do TD 2565, corrigido pelo IPCA, sobre cada ocorrência, e produzir o custo nas quatro categorias por vítima. É a variante de replicação, e ela fecha o requisito de cálculo do piloto.
