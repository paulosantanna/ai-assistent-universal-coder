---
name: ai-architecture-expert
description: Design a production AI architecture from zero or reconstruct an existing one using evidence, evals and explicit trade-offs. Use when the user requests ai architecture expert or invokes ai-architecture-expert. Do NOT use for an unrelated implementation change or deployment execution.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# AI Architecture Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

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

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
