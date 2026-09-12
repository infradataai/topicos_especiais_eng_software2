# ADR-004 — Topologia de repositórios do piloto RN e da escala nacional

Formato MADR. Numeração própria da sandbox da disciplina.

- Status: ACEITO
- Data: 2026-09-06
- Decisor: Flávio Eduardo Batista Moreira
- Relaciona-se com: ADR-003 (monólito modular), ADR-001 (ambiente de IA)

## Contexto

O Projeto Final entrega um piloto de custo social de sinistros no Rio Grande do Norte e prepara a escala do mesmo cálculo para o Brasil, na continuidade da tese. O piloto é material da disciplina e tem acesso aberto. A análise nacional ainda não está publicada e a colaboração da tese envolve quatro pessoas: o aluno, o coautor e os dois professores. A pergunta a decidir é como organizar o versionamento sem manter dois motores de cálculo que divergem, o que o ADR-003 manda evitar.

## Decisão

O piloto RN entra como a pasta `Projeto_Final` no repositório público que já existe, `topicos_especiais_eng_software2`, onde as três atividades assíncronas estão versionadas. A pasta carrega o núcleo de cálculo parametrizado pela unidade da federação, executado com `uf='RN'`, os dados do estado, os mapas, o relatório, os ADRs e os slides. A visibilidade pública é possível porque toda a entrada é dado aberto: PRF, SNV, DATASUS, Ipea e as respostas da LAI sem dado pessoal.

A escala nacional entra num repositório privado novo, `custo-social-sinistro-BR`, restrito ao aluno, ao coautor e aos dois professores. O repositório privado consome o mesmo núcleo do piloto e guarda os dados de todas as unidades da federação e a análise nacional que alimenta a tese. O resguardo protege o resultado ainda não publicado e a colaboração, porque o código é o mesmo do piloto.

O núcleo de cálculo é escrito uma vez, no piloto público, e o RN é a primeira instância dele. O repositório privado reusa esse núcleo em vez de reescrevê-lo, o que preserva o princípio de escala por parâmetro. Qualquer arquivo com dado pessoal, como o microdado do SIM do DATASUS, permanece fora do controle de versão nos dois repositórios, pela regra de `.gitignore` que a Tese_BR já aplica.

## Alternativas consideradas

A primeira alternativa criava um repositório próprio para cada frente, um público para o RN e outro privado para o Brasil, cada um com o seu código. Ela foi descartada porque duplica o motor de cálculo e cria dois códigos que divergem com o tempo, contra o ADR-003.

A segunda alternativa promovia o núcleo a um pacote público independente, `custo-social-core`, importado pelos dois repositórios. Ela resolve a duplicação, mas acrescenta um terceiro repositório e uma etapa de empacotamento agora desnecessária. Fica registrada como evolução possível, para quando a tese crescer.

## Consequências

Ganha-se um único motor de cálculo, com o RN e o Brasil compartilhando o mesmo código e o mesmo referenciamento linear. A disciplina fica num repositório só, com histórico contínuo, o que facilita a revisão pelo professor. O resultado nacional não publicado fica resguardado no repositório privado.

Perde-se, por ora, a instalação do núcleo como dependência formal: o repositório privado reusa o núcleo por cópia controlada ou submódulo, com a versão anotada, até que a promoção a pacote se justifique. O acoplamento entre o piloto e a escala passa a exigir disciplina de sincronização, mitigada pela anotação da versão do núcleo em cada repositório.
