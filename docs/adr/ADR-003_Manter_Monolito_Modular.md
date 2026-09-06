# ADR-003 — Manter o projeto como monólito modular

Formato MADR. Numeração própria da sandbox da disciplina.

- Status: ACEITO
- Data: 2026-09-06
- Decisor: Flávio Eduardo Batista Moreira
- Relaciona-se com: ADR-001 (ambiente de IA), ADR-002 (servidores MCP)

## Contexto

A Etapa 4 da atividade pediu uma revisão da arquitetura do projeto a partir do código real. O levantamento mostrou cinco módulos em `src/`, cada um com responsabilidade única, sem nenhum import entre eles, dependendo apenas de bibliotecas externas. A pergunta a decidir é se o projeto deveria ser mais modular, extrair um serviço, ou permanecer como está.

## Decisão

Manter o projeto como um monólito modular, em um único repositório e um pacote `src/`, com módulos pequenos e de fronteira clara. Não extrair serviços neste momento. Como melhoria incremental, planejar um módulo fino de acesso a dados que torne explícito o contrato de conexão com o banco e as convenções da camada bronze.

## Consequências

Ganha-se simplicidade operacional e melhor raciocínio do agente de IA, que enxerga o sistema inteiro em um contexto só, sem saltar entre repositórios. Ganha-se também facilidade de teste, já que cada módulo é isolado e verificável. Perde-se a escalabilidade independente por serviço, que não é uma necessidade atual e pode ser reavaliada quando o projeto escalar para cobertura nacional, ponto em que a troca de SQLite por DuckDB ou PostgreSQL e a eventual extração de um serviço de mapa poderão ser consideradas, cada uma com seu próprio ADR.
