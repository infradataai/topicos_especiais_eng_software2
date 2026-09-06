# Etapa 5 — Diagrama da arquitetura (duas versões)

A tarefa pediu gerar o diagrama da arquitetura e depois gerá-lo de uma segunda forma, comparando qual comunica melhor. As duas versões representam a mesma visão de contêiner (nível C4), com abordagens diferentes.

## Versão 1 — Fluxograma Mermaid (leve, renderiza em qualquer lugar)

```mermaid
flowchart TD
    subgraph entradas["Fontes de dados"]
        csv["CSV/XLSX de microdados (PRF, LAI/INSS)"]
        pdf["Respostas da LAI em PDF"]
    end
    subgraph src["Pacote src/ (monolito modular)"]
        parse["parse_datas: data deterministica"]
        loader["lai_loader: carga idempotente"]
        parser["lai_pdf_parser: extrai tabela"]
        valid["lai_validador: qualidade + contagem"]
        analise["analise: outliers + risco"]
    end
    db[("SQLite (camada bronze/consolidada)")]
    rel["Relatorios / metricas de qualidade"]

    csv --> loader --> db
    pdf --> parser --> loader
    csv --> parse
    db --> valid --> rel
    db --> analise --> rel
```

## Versão 2 — C4 Container Mermaid (padrão C4, mais formal)

```mermaid
C4Container
    title Diagrama de Conteineres - piloto de dados de sinistros
    Person(analista, "Analista", "Integra e valida os dados")
    System_Boundary(sis, "Pipeline de dados") {
        Container(ingestao, "Ingestao", "Python: lai_loader, lai_pdf_parser", "Le CSV/PDF e carrega")
        Container(qualidade, "Qualidade e analise", "Python: lai_validador, analise", "Valida, conta, detecta outliers")
        ContainerDb(banco, "Banco", "SQLite", "Camada bronze/consolidada")
    }
    System_Ext(fontes, "Orgaos publicos", "PRF, INSS, DNIT")
    Rel(fontes, ingestao, "Fornece arquivos")
    Rel(ingestao, banco, "Grava")
    Rel(qualidade, banco, "Le")
    Rel(analista, qualidade, "Consulta relatorios")
```

## Comparação

A versão 1 (fluxograma) mostra os cinco módulos individualmente e o caminho do dado, arquivo por arquivo, o que comunica melhor a granularidade real do código e renderiza sem depender de suporte a C4. A versão 2 (C4 Container) agrupa os módulos em contêineres de responsabilidade (ingestão, qualidade e banco) e explicita o ator e os sistemas externos, o que comunica melhor a intenção arquitetural para quem não vai ler o código, ao custo de esconder os módulos individuais e de exigir um renderizador com suporte a C4.

Para este projeto, a versão 1 comunica melhor no dia a dia da equipe, porque o nível de detalhe bate com o tamanho do código (cinco módulos cabem num único diagrama legível). A versão 2 seria a escolha para uma apresentação à banca ou para o artigo, onde a fronteira de responsabilidade importa mais do que o módulo específico.
