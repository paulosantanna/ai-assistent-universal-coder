---
name: ai-project-bootstrapper
description: "Bootstrap a real AI project from zero or rebuild one step by step. Use to bootstrap an AI project. Do NOT use for one-off coding."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# AI Project Bootstrapper

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

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

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
