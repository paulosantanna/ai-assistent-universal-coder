---
name: test-expert
description: "Route a test by sourced category and evidence. Use for test-expert, qa-expert or a test plan. Do NOT use for exploit payloads, invented oracles or unit-only proof."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# test-expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

O alias deste pacote é `qa-expert`. Ele substitui o papel amplo de `tests-expert`; o charter funcional e de ponta a ponta continua em [tests-expert](../tests-expert/SKILL.md).

## Quando usar

Use quando o pedido for testar, planejar teste, escolher categoria ou provar um comportamento. Se a categoria não vier no pedido, pare e pergunte. A lista está em [categorias](references/categories.md).

## Procedimento

1. Leia `07_mapeamentos` antes de editar qualquer arquivo e limite a edição ao que o pedido relaciona.
2. Rode `python qa-expert-mcp/server.py` só como MCP stdio, ou leia `qa-expert-mcp/knowledge.json` se o processo não puder subir. Não invente definição ausente.
3. Sem categoria, chame `plan_checks` sem argumento e apresente os ids. Não escolha uma.
4. Com categoria `sourced`, use só os checks e os excertos devolvidos. Com `label_only` ou `heading_only`, diga a lacuna e pergunte.
5. Para funcional e ponta a ponta observáveis, congele o charter com [tests-expert](../tests-expert/SKILL.md). Do not invent a passing check.
6. Ferramenta: `get_tool` devolve quando, onde, por que e como. O como aponta a página oficial e não traz linha de comando.
7. Segurança vista como requisito usa a categoria `security-requirement`. Exploração ofensiva é [pentests-expert](../../(security)/pentests-expert/SKILL.md), e só se for chamada.
8. Perguntas de refinamento e release: se `list_questions` vier `unavailable`, não escreva uma lista.

## Saída

Categoria, estado da fonte, checks usados, caminho da evidência e PASS ou a pergunta que falta. Um teste de unidade sozinho não é PASS.

## Exemplo

User says: "teste o login".
Result: `needs_category`. As categorias saem do MCP. Nenhuma é escolhida no lugar do usuário.

## Falha

Se o id não existir, o servidor devolve error. Não troque por uma categoria parecida. Se a fonte do glossário ISTQB continuou vazia, a definição continua ausente.

Provenance: [provenance](references/provenance.md).

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
