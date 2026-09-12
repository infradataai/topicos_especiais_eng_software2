# Post do LinkedIn — método STAR

Texto pronto para publicar.

Mídia do post: o GIF curto do mapa fica em `docs/trechos-criticos-mapa.gif` — cerca de 8 segundos, mostrando a troca da leitura (por quilômetro → por veículo-quilômetro) e um zoom num corredor crítico do RN. Roteiro de gravação em `docs/roteiro-gif-mapa.md`.

Antes de postar: anexar esse GIF e conferir o link do repositório. Depois de publicar, copiar o link do post para o `documento-de-entrega.md`.

---

**Quanto custa, por ano, um sinistro que ninguém somou no orçamento?**

No projeto final de Tópicos Avançados em Engenharia de Software 2 (PPgTI/UFRN), construímos um sistema para medir o custo social dos sinistros nas rodovias federais — e o processo importou tanto quanto o resultado.

**Situação.** O custo social dos acidentes de trânsito raramente aparece de forma acionável para quem decide onde investir em segurança viária. Os dados existem, mas chegam de vários órgãos, em formatos diferentes, e costumam ser tratados de forma agregada.

**Tarefa.** Desenvolver, em dupla, um pipeline que ingere dados heterogêneos da PRF, do SNV/DNIT e do IPEA, calcula o custo por ocorrência em quatro categorias de gravidade e entrega o resultado num mapa consultável — com ênfase em Spec-Driven Development e em harness de controle de agentes de IA.

**Ação.** Especificamos antes de codar, com OpenSpec e GitHub Spec-Kit: prompt inicial, requisitos, critérios de aceite em Given/When/Then com caso de borda, e plano de tarefas. Operamos o agente (Claude Code) em ramo isolado, com revisão de diff a cada aceite e guardrails configurados em `.claude/settings.json` que bloqueiam operações destrutivas. As decisões ficaram registradas em ADRs (formato MADR), com um diagrama de arquitetura produzido em duas formas. O núcleo fechou com 106 testes automatizados.

**Resultado.** O piloto do Rio Grande do Norte apontou R$ 1,91 bilhão de custo social no período de 2019 a 2025 (preços de jun/2026), sobre 1.666,5 km de malha crítica. A mesma lógica já roda em escala nacional, em dados preliminares. O aprendizado principal: num desenvolvimento assistido por IA, a especificação clara e o guardrail que funciona de fato pesam mais do que a escolha do modelo.

Repositório: github.com/infradataai/topicos_especiais_eng_software2

\#DesenvolvimentoAssistidoPorIA #SpecDrivenDevelopment #EngenhariaDeSoftware #SegurançaViária #DadosAbertos #PPgTI #UFRN
