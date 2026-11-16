---
name: bm25-expert
description: "Design, tune and evaluate BM25 and hybrid lexical retrieval. Use for BM25 or hybrid search work. Do NOT use for unrelated domains or deployment."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# BM25 Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Design, tune and evaluate lexical retrieval and hybrid BM25 pipelines.

## Expertise
Tokenization/analyzers, stemming/normalization, field weighting, k1/b tuning, filters, query expansion, exact identifiers, multilingual corpora, sparse retrieval, RRF/weighted fusion with dense retrieval.

## Procedure
Build lexical baseline → create judged query set → measure recall/precision/ranking → inspect failures → tune analyzers/fields/parameters one variable at a time → compare hybrid fusion → lock regression evals.

Never tune only against anecdotal queries.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
