---
name: ai-architecture-expert
description: "Design or reconstruct production AI architecture with evidence and trade-offs. Use for AI architecture. Do NOT use for deployment."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# AI Architecture Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Design a production AI architecture from zero or reconstruct an existing one using evidence, evals and explicit trade-offs.

## Architecture planes
Ingestion/governance → canonical data → retrieval/indexing → model/inference → tools/agents → policy/guardrails → evals → observability → memory → delivery/rollback.

## Decision tree
- Start with prompt + context baseline.
- Add lexical/vector/hybrid retrieval when knowledge grounding is the bottleneck.
- Add reranking when retrieval precision/ordering is limiting.
- Add fine-tuning/PEFT when behavior/style/task adaptation remains deficient after prompt/context improvements and a train/eval set exists.
- Add agents/tools only for tasks requiring actions or multi-step environment interaction.
- Every architecture has offline + online evals, security model, SLOs, cost budget and rollback.

## Outputs
Current-state map, target architecture, ADRs, implementation sequence, interfaces, data contracts, threat model, eval plan, observability and migration/rollback plan.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
