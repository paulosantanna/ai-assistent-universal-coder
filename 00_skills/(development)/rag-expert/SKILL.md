---
name: rag-expert
description: "Implement and evaluate grounded retrieval: hybrid search, reranking, citations. Use for RAG work. Do NOT use for standalone Laya training."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.1.0
  owner_agent: codenavi-agent
---

# rag-expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Outcome
Implement or repair RAG with measurable retrieval and grounding quality.

## Workflow
1. Inspect sources, document versions, ACLs and existing implementation; freeze a retrieval/answer baseline before changing it.
2. Parse, normalize and deduplicate; choose chunk boundaries from document structure and token budgets, retaining source provenance.
3. Evaluate lexical and vector retrieval, combine justified candidates, rerank and pack context without dropping citation identities.
4. Generate only from authorized active evidence; validate citation IDs, abstain when unsupported and test answer entailment separately.
5. Measure recall@k/nDCG, answer correctness, citation validity, faithfulness, latency and cost; route graph-specific work to ragraph-expert.
6. Compare the final behavior with baseline; preserve working modes and report remaining provider/evaluation uncertainty.

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
- Read [retained provenance](references/provenance.md) for the original package's migration history.
- Read [retained usage](references/usage-and-verification.md) when checking the original generic invocation contract.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
