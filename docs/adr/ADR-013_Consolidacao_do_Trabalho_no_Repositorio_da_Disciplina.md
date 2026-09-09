# ADR-013 - Consolidação do trabalho no repositório da disciplina

Formato MADR. Numeração própria da sandbox da disciplina.

- Status: ACEITO
- Data: 2026-09-09
- Decisores: Flávio Eduardo Batista Moreira e Bruno dos Santos Fernandes da Silva
- Relaciona-se com: ADR-003 (monólito modular), ADR-004 (topologia de repositórios)
- Substitui: ADR-010 (repositório de trabalho único)

## Contexto

O ADR-004 previu duas casas para o trabalho: o piloto do Rio Grande do Norte, público,
e a escala nacional, privada. O ADR-010 escolheu `custo-social-sinistro-BR` como
repositório de trabalho corrente. Nos dias 8 e 9 de setembro os dois autores
implementaram em repositórios distintos, sem que a divisão fosse combinada.

O levantamento mediu o que cada lado produziu. Em `topicos_especiais_eng_software2`,
na branch `feature/projeto-final-rn`, estão os módulos `analise.py`, `consulta_web.py`
e `relatorios.py`, o carregador da LAI ampliado e a migração do OpenSpec para a
estrutura da linha de comando, que somam 6.410 inserções e 30 testes. Em
`custo-social-sinistro-BR` está o núcleo de dados: ingestão da PRF, produto escalar do
custo, ancoragem no SNV, exposição do PNCT, agregados do DATASUS e persistência, com
12 módulos e 76 testes. A apresentação ocorre em 12 de setembro, sem prorrogação.

Os dois conjuntos se completam por área, e a comparação arquivo a arquivo encontrou
sete caminhos coincidentes. Dois deles bloqueiam a junção. A numeração dos registros de
decisão colidiu: cada lado criou um ADR-006, um ADR-007 e um ADR-008, com conteúdos
diferentes. E o `.gitignore` da branch não cobre a pasta `dados/` nem as extensões do
DATASUS, o mesmo defeito que em 7 de setembro levou 378 arquivos de microdado do SIM,
com 807 MB, para o controle de versão do outro repositório.

## Decisão

O trabalho passa a residir em `topicos_especiais_eng_software2`, na branch
`feature/projeto-final-rn`. A consolidação segue seis regras.

**Sentido da migração.** O núcleo de dados vai para o repositório da disciplina, e não o
contrário. Aquele repositório guarda o histórico dos dois autores desde a primeira
atividade, hospeda a estrutura do OpenSpec com a linha de comando e é o endereço que a
avaliação abre.

**Local do pacote.** O pacote `custo_social_core` fica na raiz, ao lado de `src`, sem
fusão. Fundir os dois obrigaria a reescrever os importes dos 76 testes e das quatro
mudanças do OpenSpec, com risco na véspera da entrega e sem ganho para o leitor. O
ADR-003 mantém o monólito modular, e dois pacotes de fronteira clara o respeitam.

**Numeração dos registros.** Os registros do núcleo de dados passam a ADR-009
(ingestão determinística da PRF), ADR-010 (repositório de trabalho, agora substituído
por este), ADR-011 (parâmetros do cálculo) e ADR-012 (decomposição em três eixos). As
vinte referências cruzadas foram remapeadas na mesma passagem. Nos ADR-002 e ADR-003,
que divergiram entre as cópias, prevalece a versão da branch, que é superconjunto da
outra.

**Formato do OpenSpec.** As quatro mudanças do núcleo migram para o padrão datado já
adotado na branch, em `openspec/changes/archive/`, e as suas seis capacidades sobem
para `openspec/specs/`. O repositório passa a declarar onze capacidades sob o mesmo
esquema.

**Dados versionados.** O `.gitignore` bloqueia `dados/` e as extensões de origem,
entre elas `.dbc` e `.dbf`, com uma exceção declarada: `dados/consolidado.db`, o banco de
8,5 MB que a aplicação consome. Sem ele a demonstração não roda em outra máquina. Os
35 GB de arquivos de origem permanecem fora, e são reproduzíveis pelos scripts de
ingestão.

**Esqueleto anterior.** A pasta `Projeto_Final` guardava o esqueleto do núcleo, com seis
módulos de assinatura sem implementação, criado antes da fase 2. O pacote da raiz o
cobre inteiramente, com implementação e testes, e o esqueleto sai para que não restem
duas versões do mesmo módulo. Permanecem no diretório o escopo e o `README`.

O `custo-social-sinistro-BR` conserva o papel que o ADR-004 lhe deu: a caixa privada da
escala nacional, onde ficam os arquivos de origem e onde a ingestão do RENAEST será
executada depois da apresentação.

## Alternativas consideradas

**Migrar o trabalho do outro autor para `custo-social-sinistro-BR`.** Descartada porque
o repositório da disciplina carrega o histórico das atividades avaliadas e a estrutura
do OpenSpec com a linha de comando. A migração no sentido inverso descartaria esse
histórico ou exigiria transplantá-lo.

**Manter os dois repositórios e sincronizar por cópia.** Descartada por duplicar o ponto
de verdade três dias antes da entrega. A divergência entre as cópias do `contratos.md` e
dos ADR-002 e ADR-003, já observada, mostra o custo dessa rota.

**Fundir `custo_social_core` dentro de `src`.** Descartada pelo custo de reescrever os
importes de 76 testes e de quatro pacotes de especificação no prazo disponível. A fusão
fica disponível como limpeza posterior, sem urgência.

**Renumerar os registros do outro autor em vez dos nossos.** Descartada porque os ADR-005
a ADR-008 da branch já são citados pelo ADR-003 e pelas especificações arquivadas, e
renumerá-los propagaria a correção por mais arquivos.

## Consequências

O repositório passa a ter um ponto de verdade, com 106 testes na mesma execução, 14
registros de decisão em numeração contínua e onze capacidades declaradas no OpenSpec.

A camada de aplicação ganha acesso ao banco de sinistros. Os módulos `analise.py` e
`relatorios.py` são genéricos quanto à tabela e ao dicionário de entrada, e passam a
operar sobre as tabelas do núcleo sem alteração. O `consulta_web.py` consulta o esquema
da LAI, com as tabelas `fontes`, `lotes` e `registros_canonicos`, e por isso exige rotas
novas para as tabelas de ocorrência, custo e segmento. Essa é a tarefa que resta para
fechar o requisito da consulta web com mapa.

Assume-se o custo de manter dois pacotes na raiz até que a fusão seja feita, e o de
versionar um binário de 8,5 MB, cuja alteração aparece no histórico como arquivo
substituído.

## Verificação

A suíte consolidada roda em uma única execução: 106 testes aprovados, 30 da camada
de aplicação e 76 do núcleo de dados. A regra do `.gitignore` foi conferida contra a
listagem real dos 970 arquivos da pasta de dados, e não apenas contra o padrão escrito.

## Reversibilidade

Média. Desfazer a consolidação significaria separar de novo dois conjuntos que passam a
compartilhar o mesmo esquema de numeração e o mesmo OpenSpec. O que não se reverte sem
prejuízo é a exceção do `.gitignore`: qualquer alargamento dela reabre a porta pela qual
os 807 MB de microdado entraram uma vez.
