---
name: bm25-expert
description: Design, tune and evaluate lexical retrieval and hybrid BM25 pipelines. Use when the user requests bm25 expert or invokes bm25-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# BM25 Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

## Mission
Design, tune and evaluate lexical retrieval and hybrid BM25 pipelines.

## Expertise
Tokenization/analyzers, stemming/normalization, field weighting, k1/b tuning, filters, query expansion, exact identifiers, multilingual corpora, sparse retrieval, RRF/weighted fusion with dense retrieval.

## Procedure
Build lexical baseline → create judged query set → measure recall/precision/ranking → inspect failures → tune analyzers/fields/parameters one variable at a time → compare hybrid fusion → lock regression evals.

Never tune only against anecdotal queries.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
