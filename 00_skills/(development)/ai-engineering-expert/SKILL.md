---
name: ai-engineering-expert
description: "Build or refactor production AI systems from requirements to monitored deployment. Use for AI engineering. Do NOT use for unrelated domains."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# AI Engineering Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Build or refactor production AI systems end-to-end from requirements to monitored deployment.

## Coverage
Problem framing, dataset contracts, model/provider selection, prompting, structured outputs, tool use/agents, RAG, embeddings, reranking, fine-tuning/PEFT, evals, safety, latency/cost, caching, observability, drift and rollback.

## Deterministic build sequence
1. Define business task and failure cost.
2. Create golden set and baseline.
3. Choose simplest architecture capable of target quality.
4. Implement data/model interfaces behind adapters.
5. Add eval harness before optimization.
6. Add RAG/fine-tuning only when eval evidence justifies it.
7. Threat-model prompt injection/data leakage/tool abuse.
8. Load/performance/cost test.
9. Shadow/canary deployment when risk warrants.
10. Monitor quality and operational metrics; preserve rollback.

Current model/API availability must be verified from authoritative sources at execution time; never hardcode a 'latest' model as timeless truth.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
