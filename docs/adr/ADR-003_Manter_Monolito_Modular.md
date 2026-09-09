# ADR-003 — Manter o projeto como monólito modular

Formato MADR. Numeração própria da sandbox da disciplina.

- Status: ACEITO
- Data: 2026-09-06
- Decisor: Flávio Eduardo Batista Moreira
- Relaciona-se com: ADR-001 (ambiente de IA), ADR-002 (servidores MCP)

## Contexto

A Etapa 4 da atividade pediu uma revisão da arquitetura do projeto a partir do código real. O levantamento inicial mostrou cinco módulos em `src/`, cada um com responsabilidade única. A evolução especificada no OpenSpec acrescenta ingestão multi-origem, análise estatística, consulta web e geração de relatórios. A pergunta a decidir é se essas capacidades exigem serviços separados ou se devem permanecer em um monólito modular.

## Decisão

Manter o projeto como um monólito modular, em um único repositório e um pacote `src/`, com módulos pequenos e de fronteira clara para ingestão, qualidade, análise, consulta e relatórios. Não extrair serviços neste momento. O acesso ao SQLite deve ser mediado por um módulo de dados compartilhado, sem permitir que a camada web ou a análise alterem a cópia bronze.

## Consequências

Ganha-se simplicidade operacional e melhor raciocínio do agente de IA, que enxerga o sistema inteiro em um contexto só, sem saltar entre repositórios. Ganha-se também facilidade de teste, já que cada módulo é isolado e verificável. A consulta web e a geração de relatórios permanecem fronteiras de aplicação, não serviços independentes. Perde-se a escalabilidade independente por serviço, que pode ser reavaliada quando a carga nacional justificar a troca de SQLite ou a extração de um serviço, cada uma com seu próprio ADR. As decisões específicas de dados, análise, web e relatórios estão nos ADR-005 a ADR-008.
