---
name: rag-expert
description: Implement or repair Retrieval-Augmented Generation systems with measurable grounding quality. Use when the user requests rag expert or invokes rag-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# RAG Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Implement or repair Retrieval-Augmented Generation systems with measurable grounding quality.

## Build path
Source authority/provenance → parsing → normalization/dedup → chunk strategy → metadata/ACLs → lexical + vector indexes → query rewrite when justified → retrieval → fusion → rerank → context packing → grounded generation → citations → evals/monitoring.

## Metrics
Recall@k, precision@k, MRR/nDCG where appropriate, answer correctness, faithfulness/groundedness, citation validity, latency and cost.

Use BM25 + embeddings as a strong hybrid baseline when corpus/query characteristics justify both lexical exactness and semantic recall. Prevent cross-tenant/ACL leakage before quality optimization.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
