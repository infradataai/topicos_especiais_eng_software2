# Spec (delta) - consulta

## ADDED Requirements

### Requirement: Marcação de qualidade geodésica pela faixa de domínio
O sistema DEVE medir a distância de cada sinistro ao eixo da sua BR, com a geometria
oficial do SNV em resolução cheia, e DEVE gravar uma marca indicando se o sinistro
está dentro de uma faixa de domínio de 50 metros para cada lado.

#### Scenario: Sinistro sobre a via
- **GIVEN** um sinistro cuja coordenada está a menos de 50 metros do eixo da BR
- **WHEN** a marcação é executada
- **THEN** o sinistro é marcado como dentro da faixa

#### Scenario: Sinistro deslocado do eixo
- **GIVEN** um sinistro cuja coordenada está a mais de 50 metros do eixo da BR
- **WHEN** a marcação é executada
- **THEN** o sinistro é marcado como fora da faixa

### Requirement: Filtro do mapa pela faixa de domínio
O mapa DEVE desenhar apenas os sinistros dentro da faixa de domínio, quando a marca
de qualidade estiver calculada. O custo e a contagem por segmento NÃO mudam, porque
consideram todos os sinistros ancorados.

#### Scenario: Marca calculada
- **GIVEN** um banco com a marca de qualidade calculada
- **WHEN** os pontos do mapa são consultados
- **THEN** apenas os sinistros dentro da faixa são devolvidos

#### Scenario: Marca ausente
- **GIVEN** um banco sem a marca de qualidade
- **WHEN** os pontos do mapa são consultados
- **THEN** todos os sinistros são devolvidos, para o mapa não ficar vazio
