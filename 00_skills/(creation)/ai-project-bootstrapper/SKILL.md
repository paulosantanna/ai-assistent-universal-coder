---
name: ai-project-bootstrapper
description: Implement a real AI project from zero or reconstruct an existing project step-by-step using the specialist skill pack. Use when the user requests ai project bootstrapper or invokes ai-project-bootstrapper. Do NOT use for ordinary one-off coding or human competency lists.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# AI Project Bootstrapper

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Implement a real AI project from zero or reconstruct an existing project step-by-step using the specialist skill pack.

## Greenfield sequence
1. Business/problem contract and risk classification.
2. Repository/toolchain/security baseline.
3. Dataset/source governance and schemas.
4. Golden eval set before architecture optimization.
5. Baseline model/prompt implementation.
6. Retrieval: BM25/vector/hybrid only when needed.
7. Reranking/context engineering.
8. Fine-tuning/LoRA/QLoRA/DoRA only after eval gate.
9. API/tool/agent integration.
10. Guardrails, auth, tenant/data isolation.
11. Observability: traces, retrieval/model metrics, cost, quality.
12. Offline/online evals and adversarial tests.
13. Shadow/canary release, rollback and documentation.

## Existing-project sequence
Map current architecture/data/models/prompts/retrieval/evals → reproduce baseline → identify bottleneck by evidence → target architecture/ADR → migrate in reversible slices → compare each slice against baseline → retire legacy only after parity/target gates.

Composes: ai-architecture-expert, ai-engineering-expert, rag-expert, bm25-expert, fine-tuning-expert, lora-qlora-dora-expert, ai-evals-expert, llm-model-selection-expert, python-expert, security/evaluator skills.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
