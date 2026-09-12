# Projeto Final — Piloto RN de custo social de sinistros

Piloto que calcula o custo social dos sinistros nas rodovias federais do Rio Grande do Norte e projeta em mapa os trechos críticos. O mesmo código, parametrizado pela unidade da federação, é o que escala para o Brasil na continuidade da tese. O piloto é o Brasil rodado com o filtro `uf='RN'`.

## Estrutura

O núcleo saiu desta pasta e passou para a raiz do repositório na consolidação de 9 de
setembro, registrada no `docs/adr/ADR-013_Consolidacao_do_Trabalho_no_Repositorio_da_Disciplina.md`.
O esqueleto que ficava aqui tinha assinatura sem implementação, e o pacote da raiz o
cobre inteiro, com testes.

```
custo_social_core/          nucleo parametrizado por UF, na raiz do repositorio
  config.py                 a UF e o parametro de escala
  ingestao_prf.py           leitura dos arquivos anuais da PRF em quatro graos
  vetor_m.py                Tabela 1 do Ipea, mapa de veiculos, deflator
  custo.py                  produto escalar C x M, com as quatro categorias
  snv.py                    leitura das safras e ancoragem por referencia linear
  exposicao.py              VMDa do PNCT, veiculos-km e criticidade
  saude.py                  agregados do DATASUS e cobertura de jurisdicao
  persistencia.py           esquema SQLite de 11 tabelas, com proveniencia
  referenciamento.py        primitivas de safra e segmento
  subregistro.py            cenarios de correcao, hoje governados pelo ADR-012
  pipeline.py               orquestrador: UF -> tabela por segmento
scripts/
  reconstruir_prf.py        reconstrucao da base da PRF a partir dos arquivos anuais
  consolidar_e_ancorar.py   carga do banco consolidado de uma UF
  run_nacional.py           a mesma logica nas 27 unidades da federacao
tests/                      76 testes do nucleo, ao lado dos 30 da aplicacao
dados/consolidado.db        banco consolidado, versionado por excecao declarada
Projeto_Final/
  Escopo_Projeto_Final_RN_BR.md   escopo completo, revisado
  README.md                       este arquivo
```

## Como rodar

```bash
# na raiz do repositorio
python -m pytest -q                                  # 106 testes
python scripts/consolidar_e_ancorar.py --uf RN       # reconstroi o banco do RN
python -m src.consulta_web                           # sobe a consulta web
```

A carga completa precisa dos arquivos de origem, que ficam fora do controle de versão.
Para consultar sem refazer a carga, o `dados/consolidado.db` já acompanha o repositório.

## Decisões e escopo

A topologia de repositórios está no `docs/adr/ADR-004_Topologia_Repositorios.md`, e a consolidação do trabalho neste repositório está no `docs/adr/ADR-013_Consolidacao_do_Trabalho_no_Repositorio_da_Disciplina.md`. O `custo-social-sinistro-BR` permanece como a caixa privada da escala nacional, onde ficam os arquivos de origem. A arquitetura de monólito modular está no `docs/adr/ADR-003_Manter_Monolito_Modular.md`. O escopo completo, com o modelo de custo, a espacialização e o plano por fases, está em `Escopo_Projeto_Final_RN_BR.md`.

## Dados e privacidade

Toda a entrada é dado aberto: PRF, SNV, DATASUS, Ipea e as respostas da LAI sem dado pessoal. Qualquer arquivo com dado pessoal, como o microdado do SIM, fica fora do controle de versão, pela regra de `.gitignore` do projeto.

## Fases

1. Modelo de custo em quatro categorias, com decomposição da classe de feridos e triangulação contra o Ipea, sobre os dados do RN.
2. Espacialização: referenciamento linear dos sinistros do RN nos segmentos do SNV, com safra casada.
3. Mapa dos trechos críticos, nas duas leituras de custo por quilômetro e custo por exposição, com a camada de subregistro.
4. Relatório e apresentação, no formato das atividades anteriores.
