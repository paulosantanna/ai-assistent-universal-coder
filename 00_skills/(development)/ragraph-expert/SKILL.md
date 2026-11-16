---
name: ragraph-expert
description: "Build and evaluate source-backed knowledge-graph retrieval (GraphRAG). Use for GraphRAG or entity resolution. Do NOT use for generic diagrams."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 0.1.0
  owner_agent: codenavi-agent
---

# ragraph-expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Outcome
Build source-backed GraphRAG with temporal provenance and observable incremental updates.

## Workflow
1. Inspect corpus questions and hybrid baseline; decide whether entity relationships, temporal queries or global themes justify a graph.
2. Inspect the pinned engine API and supported database; Graphiti/Neo4j is the current package default, other engines remain explicit alternatives.
3. Extract entities/relations with validated structured outputs; resolve identity conservatively and preserve source episode IDs and validity windows.
4. Persist incremental updates and provenance before publishing graph events; keep partial/removed documents out of answer evidence.
5. Recover bounded relevant subgraphs, highlight retrieved paths and expose source details with accessible tables and reconnectable events.
6. Compare graph retrieval with the same hybrid queries; verify updates, contradictory facts, deletion, idempotence and event replay.

## Inputs, outputs and stop
Inputs: authorized corpus/project, source identities, actual runtime capabilities and frozen evaluation goal.
Outputs: source-backed artifacts, relevant runtime behavior/checkpoints and reproducible verification evidence.
Missing source/license/runtime/permission blocks the dependent step; continue independent authorized work.
Never persist credentials, claim unrun checks passed or create another agent identity.

## Modules — progressive disclosure
- Read [intake and gates](references/intake.md) before a material mission or choosing providers.
- Read [technical procedure](references/procedure.md) for implementation, analysis or troubleshooting.
- Read [runtime integration](references/runtime.md) when invoking the MCP, API or live graph.
- Read [evaluation](references/evaluation.md) before accepting quality or training results.
- Read [examples and failures](references/examples.md) for concrete invocation or a failed prerequisite.
- Read [sources and attribution](references/sources.md) when verifying facts, APIs or upstream versions.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
