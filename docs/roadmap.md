**Universidade Federal do Rio Grande do Norte**
**Instituto Metrópole Digital**
**Programa de Pós-Graduação em Tecnologia da Informação**
**Disciplina:** Tópicos Avançados em Engenharia de Software 2 (Desenv. de Software com IA)
**Professor:** Jean Mário Moreira de Lima
**Alunos:** Flávio Eduardo Batista Moreira e Bruno dos Santos Fernandes da Silva

# Roadmap do Projeto Final

## Plataforma de consolidação e análise de dados de acidentes rodoviários, com o custo social do RN como demonstração

---

## 1. O que o professor exige

A especificação define um sistema completo e funcional, com no mínimo dez requisitos funcionais demonstráveis, apresentado ao vivo em 12/09, sem prorrogação. A ênfase recai sobre o processo de desenvolvimento assistido por IA: desenvolvimento guiado por especificação, harness com guardrail que barra de fato, observabilidade, um ADR, um diagrama, controle de versão com histórico real e testes automatizados. A entrega inclui o repositório com acesso ao professor, a apresentação, um documento das ferramentas de IA usadas e um post no LinkedIn pelo método STAR.

A nota se distribui em sistema e requisitos (2,0), processo de SDD (2,0), harness aplicado de fato (2,0), arquitetura com ADR e diagrama (1,5), demonstração ao vivo (1,0), qualidade da apresentação (1,0) e entregáveis completos (0,5). As exigências são o piso, e as aulas servem de guia; o custo social do RN e a consulta em linguagem natural entram como diferencial de criatividade e pertinência, o critério de maior peso.

## 2. O escopo declarado no checkpoint

O e-mail de 05/09 fixou o escopo com o professor: um software para processar, consolidar e analisar dados heterogêneos de acidentes rodoviários de múltiplos órgãos públicos, com uma base integrada para apoiar políticas de segurança viária e a alocação de recursos de saúde. Os nove requisitos declarados foram ingestão de CSV e XLSX de vários órgãos, normalização e deduplicação, validação de tipos e detecção de inconsistências, consolidação em banco relacional único, análise estatística descritiva, detecção de outliers, rastreamento de origem, consulta web interativa e geração de relatórios em JSON e PDF. A stack declarada foi Python com FastAPI, Pydantic, Pandas, NumPy, Scikit-learn, SQLAlchemy, Pytest e Mypy. O roadmap parte desse escopo e o cumpre, com o custo social do RN por cima.

## 3. Onde já estamos

O trabalho começa com vantagem, porque os módulos do pipeline M-LRSDI já cobrem boa parte dos requisitos declarados. O `lai_loader` faz a carga idempotente, o que atende a deduplicação. O `lai_validador` valida tipos e conta inconsistências. O `parse_datas` normaliza datas com determinismo. O `analise` detecta outliers por IQR. O `custo_social_core` calcula o custo por segmento, parametrizado por UF. O servidor MCP de SQLite já consulta a camada consolidada em linguagem natural.

Os artefatos de processo que a especificação cobra também já existem, das três atividades assíncronas: o hook `block_data_commit.py` com bloqueio real, o log de sessão, as specs em OpenSpec e Spec-Kit, os ADR-001 a ADR-004, o diagrama em duas versões e o histórico de commits por etapa, com git worktrees documentados.

O que falta é montar a camada de ingestão de múltiplos órgãos, a API, o front-end da consulta web, os relatórios e o mapa do custo social, além de escrever a spec, o ADR e a demo próprios do projeto.

## 4. Decisões a confirmar antes de executar

O checkpoint de 05/09 está cumprido. O e-mail foi enviado ao professor no prazo, com os nomes, as matrículas, o escopo, os requisitos e a stack.

A stack segue a declarada no e-mail, com uma simplificação a decidir. O e-mail cita FastAPI e Django ao mesmo tempo, e os dois cobrem o mesmo papel de servir a aplicação. A recomendação é ficar com FastAPI e SQLAlchemy, que são mais leves para uma API com contrato claro, e dispensar o Django, para não inflar o escopo no prazo curto. A justificativa da plataforma web e da fronteira entre a API e o front-end entra no ADR-005.

## 5. Os requisitos funcionais do sistema

O sistema entrega, no mínimo, os seguintes requisitos funcionais, todos demonstráveis, alinhados ao escopo do checkpoint:

1. Ingestão de arquivos CSV e XLSX de múltiplos órgãos (PRF, SNV, DNIT, LAI e DATASUS), com detecção de formato, separador e codificação.
2. Normalização dos esquemas heterogêneos para um modelo comum.
3. Deduplicação idempotente dos registros.
4. Validação de tipos e detecção de inconsistências.
5. Consolidação em banco relacional único, pela camada medalhão.
6. Rastreamento de origem e versão de cada fonte, por órgão e safra.
7. Análise estatística descritiva por recorte: média, mediana e desvio padrão.
8. Detecção automática de outliers.
9. Consulta web interativa, com o mapa dos trechos críticos do RN.
10. Geração de relatórios estruturados em JSON e PDF.
11. Cálculo do custo social por segmento, com criticidade por exposição e correção de subregistro, como análise carro-chefe.
12. Consulta em linguagem natural pelo servidor MCP, sobre a base consolidada.

Os dez primeiros cumprem a exigência mínima e o escopo declarado. O décimo primeiro e o décimo segundo entram como diferencial, e ligam o projeto à tese.

## 6. Arquitetura e stack

O sistema segue o monólito modular do ADR-003, na organização medalhão. A ingestão lê os arquivos dos órgãos e grava a camada bronze imutável. A consolidação normaliza, deduplica, valida e grava a camada consolidada em SQLite por SQLAlchemy. A análise roda a estatística descritiva, os outliers e o custo social do RN sobre a camada consolidada. A API em FastAPI expõe as consultas e as análises, com os contratos validados por Pydantic. O front-end consome a API e desenha o mapa dos trechos críticos. Os relatórios saem em JSON e PDF. A escolha da stack e da fronteira entre as camadas entra no ADR-005.

## 7. Roadmap dia a dia

**06/09, domingo.** Escrever a spec do sistema em OpenSpec, com o prompt inicial, os dez requisitos, os critérios Given-When-Then e um caso de borda. Abrir o ADR-005 da stack. Dividir o trabalho da dupla por domínio, com um em ingestão e consolidação e outro em análise e API.

**07/09, segunda.** Montar a ingestão de múltiplos órgãos sobre os módulos existentes, com a detecção de formato e a gravação da camada bronze. Consolidar em banco único por SQLAlchemy. Testes da carga, da deduplicação e da validação.

**08/09, terça.** Implementar o rastreamento de origem por órgão e safra. Rodar a análise descritiva e os outliers sobre a base consolidada. Fechar o custo social do RN por segmento, com a criticidade por exposição e o subregistro. Testes das análises.

**09/09, quarta.** Construir a API em FastAPI, com os endpoints de consulta, análise e ranque de trechos. Validar os contratos com Pydantic. Testes dos endpoints. Iniciar o front-end da consulta web.

**10/09, quinta.** Concluir o mapa interativo do RN, com as duas leituras e os filtros. Implementar os relatórios em JSON e PDF. Ligar o servidor MCP à base consolidada. Ensaiar a demonstração de ponta a ponta.

**11/09, sexta.** Orientação de projetos. Montar a apresentação com os sete pontos exigidos. Escrever o documento de modelos e ferramentas de IA. Redigir o post do LinkedIn pelo método STAR. Revisar o repositório, o histórico de commits e a cobertura de testes.

**12/09, sábado.** Apresentação. Ensaio final da demo pela manhã, envio do documento de entrega com os links do repositório e do post, e defesa.

## 8. Cobertura da rubrica

Sistema e dez requisitos, peso 2,0: os doze requisitos da seção 5, com a demo ao vivo. Processo de SDD, peso 2,0: a spec em OpenSpec do dia 06, mais as specs das assíncronas. Harness aplicado de fato, peso 2,0: o hook `block_data_commit.py` com bloqueio real, o nível de autonomia justificado e o log de sessão. Arquitetura com ADR e diagrama, peso 1,5: o ADR-005 da stack, os ADR anteriores e o diagrama C4 e Mermaid. Demonstração ao vivo, peso 1,0: o roteiro do dia 10. Qualidade da apresentação, peso 1,0: os slides do dia 11. Entregáveis completos, peso 0,5: o repositório com acesso ao professor, a apresentação, o documento de ferramentas e o post do LinkedIn.

## 9. Entregáveis e checklist final

- Repositório público da disciplina com a plataforma e o histórico de commits real.
- Spec do sistema em OpenSpec, com critérios de aceite e caso de borda.
- ADR-005 da stack e diagrama da arquitetura.
- Guardrail com evidência de bloqueio e log de sessão do agente.
- Testes automatizados cobrindo ingestão, consolidação, análise e API.
- Aplicação web com a consulta, o mapa dos trechos críticos e a demo ensaiada.
- Relatórios em JSON e PDF.
- Apresentação com os sete pontos da seção V da especificação.
- Documento de modelos, estratégias e ferramentas de IA.
- Post no LinkedIn pelo método STAR, com captura de tela ou GIF da demo.
- Documento de entrega com os nomes e os links do repositório e do post.
