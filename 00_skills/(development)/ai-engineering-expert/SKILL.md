---
name: ai-engineering-expert
description: Build or refactor production AI systems end-to-end from requirements to monitored deployment. Use when the user requests ai engineering expert or invokes ai-engineering-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# AI Engineering Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

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

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
