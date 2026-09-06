# Projeto Final — Piloto RN de custo social de sinistros

Piloto que calcula o custo social dos sinistros nas rodovias federais do Rio Grande do Norte e projeta em mapa os trechos críticos. O mesmo código, parametrizado pela unidade da federação, é o que escala para o Brasil na continuidade da tese. O piloto é o Brasil rodado com o filtro `uf='RN'`.

## Estrutura

```
Projeto_Final/
  Escopo_Projeto_Final_RN_BR.md     escopo completo, revisado
  custo_social_core/                nucleo parametrizado por UF
    config.py                       a UF e o unico parametro de escala
    referenciamento.py              ancora o sinistro ao segmento do SNV (safra casada)
    custo.py                        custo hibrido em 4 categorias (Ipea ancora + LAI)
    exposicao.py                    criticidade ajustada por exposicao (PNCT/VMDa)
    subregistro.py                  correcao PRF -> SIM por cenario
    pipeline.py                     orquestrador: UF -> tabela por segmento
  scripts/run_pilot.py              ponto de entrada (RN por padrao)
  tests/test_nucleo.py              testes de logica pura + pipeline com provedor falso
  docs/contratos.md                 contratos EARS de cada modulo
```

## Como rodar

```bash
# na raiz do repositorio
python -m Projeto_Final.scripts.run_pilot            # roda o RN
python -m Projeto_Final.scripts.run_pilot --uf PB    # a mesma logica, outra UF
python -m pytest Projeto_Final/tests/ -q             # testes
```

O `run_pilot` usa hoje um provedor de demonstração, para exercitar o fluxo. A leitura dos dados reais (PRF, SNV, VMDa, LAI) entra na fase 2, por uma implementação de `ProvedorDeDados`.

## Decisões e escopo

A topologia de repositórios está no `docs/adr/ADR-004_Topologia_Repositorios.md`: o piloto RN é público, neste repositório; a escala nacional é o repositório privado `custo-social-sinistro-BR`, que reusa este núcleo. A arquitetura de monólito modular está no `docs/adr/ADR-003_Manter_Monolito_Modular.md`. O escopo completo, com o modelo de custo, a espacialização e o plano por fases, está em `Escopo_Projeto_Final_RN_BR.md`.

## Dados e privacidade

Toda a entrada é dado aberto: PRF, SNV, DATASUS, Ipea e as respostas da LAI sem dado pessoal. Qualquer arquivo com dado pessoal, como o microdado do SIM, fica fora do controle de versão, pela regra de `.gitignore` do projeto.

## Fases

1. Modelo de custo em quatro categorias, com decomposição da classe de feridos e triangulação contra o Ipea, sobre os dados do RN.
2. Espacialização: referenciamento linear dos sinistros do RN nos segmentos do SNV, com safra casada.
3. Mapa dos trechos críticos, nas duas leituras de custo por quilômetro e custo por exposição, com a camada de subregistro.
4. Relatório e apresentação, no formato das atividades anteriores.
