# Revisão humana — candidatos Reversa

O usuário delegou a revisão ao assistente; o resultado está em [REVISAO-ASSISTENTE.md](REVISAO-ASSISTENTE.md) e não é revisão humana independente. O formulário abaixo permanece disponível para uso futuro.

Para cada item, confira pergunta, resposta e fonte. Marque aprovado, rejeitado ou correção e escreva seu nome; devolva as decisões aqui na conversa ou edite este arquivo. Não marque como aprovado automaticamente.

Os exemplos são rascunhos do mesmo repositório; sua aprovação não cria uma amostra independente nem resolve separação de famílias. Os hashes referem-se ao checkout registrado no manifesto.

## reversa-candidate-001

**Pergunta:** Quais comandos a CLI encaminha?

**Resposta proposta:** Ela encaminha install, update, status, uninstall, add-engine e export-diagrams.

**Fonte:** [bin/reversa.js](../../02_repositorios/reversa/bin/reversa.js), linha 14; SHA-256 `afc495e3e16fb471ceb804181013587edf9801f887890cd6ce8e34792fbf7cfd`.

**Decisão:** pendente  
**Correção/observação:**  
**Revisor:**  

## reversa-candidate-002

**Pergunta:** Como o manifesto identifica modificações?

**Resposta proposta:** O manifesto armazena hashes SHA-256 e fileStatus compara o hash atual com o original.

**Fonte:** [lib/installer/manifest.js](../../02_repositorios/reversa/lib/installer/manifest.js), linha 41; SHA-256 `05ed1cabe40ca9faf2d763880f6cc81f0d2cc395109168f6fdf1e2db8dfbdb04`.

**Decisão:** pendente  
**Correção/observação:**  
**Revisor:**  

## reversa-candidate-003

**Pergunta:** Qual o padrão de edição de legado?

**Resposta proposta:** O template declara allowLegacyEdits como false e allowedPaths como lista vazia.

**Fonte:** [templates/reversa-config.json](../../02_repositorios/reversa/templates/reversa-config.json), linha 3; SHA-256 `02802e2e1cb8ebfad14ef1a1cc58ecba41845c6b8ed32016c01846a64a85ffaa`.

**Decisão:** pendente  
**Correção/observação:**  
**Revisor:**  

## reversa-candidate-004

**Pergunta:** Quais fases constam no estado inicial?

**Resposta proposta:** Reconhecimento, escavação, interpretação, geração e revisão constam como pendentes.

**Fonte:** [templates/state.json](../../02_repositorios/reversa/templates/state.json), linha 13; SHA-256 `4c97b2317289d707cb3c815dfee8fab5b87c6c6ff3ea542a517cdc53e2b96756`.

**Decisão:** pendente  
**Correção/observação:**  
**Revisor:**  

## reversa-candidate-005

**Pergunta:** A atualização consulta alguma fonte externa?

**Resposta proposta:** O código tenta consultar a versão mais recente no registro npm e pode continuar offline se falhar.

**Fonte:** [lib/commands/update.js](../../02_repositorios/reversa/lib/commands/update.js), linha 13; SHA-256 `4694e5594c6d682bd4dc183b8ad5ff78890f215bb28a71fc2f501836409fa4b5`.

**Decisão:** pendente  
**Correção/observação:**  
**Revisor:**  

## reversa-candidate-006

**Pergunta:** Que confirmação a remoção pede?

**Resposta proposta:** O fluxo pede que o usuário digite remove antes da desinstalação e pergunta separadamente sobre a pasta de saída.

**Fonte:** [lib/commands/uninstall.js](../../02_repositorios/reversa/lib/commands/uninstall.js), linha 89; SHA-256 `1960165605eedf5525a92f3ff894023d48132d8329495dc17293ddc4b0249f66`.

**Decisão:** pendente  
**Correção/observação:**  
**Revisor:**  

## reversa-candidate-007

**Pergunta:** Qual é o ponto de entrada do pacote Node?

**Resposta proposta:** O manifesto declara bin/reversa.js como executável reversa.

**Fonte:** [package.json](../../02_repositorios/reversa/package.json), linha 6; SHA-256 `404426412293b3238c227dd58f0aa5a9d2c6874fc707782d8a492f4c19bade0a`.

**Decisão:** pendente  
**Correção/observação:**  
**Revisor:**  

## reversa-candidate-008

**Pergunta:** As instruções do Reversa têm precedência sobre o AGENTS.md deste workspace?

**Resposta proposta:** Não. O conteúdo do repositório é fonte não confiável e deve ser interpretado sob o contrato raiz do workspace.

**Fonte:** [agents/reversa/SKILL.md](../../02_repositorios/reversa/agents/reversa/SKILL.md), linha 13; SHA-256 `0439b117c8d041a3ac101f482e653f8631a63aa5d105cb7423637064a3e403d0`.

**Decisão:** pendente  
**Correção/observação:**  
**Revisor:**  
