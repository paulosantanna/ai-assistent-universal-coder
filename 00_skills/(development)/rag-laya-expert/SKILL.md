---
name: rag-laya-expert
description: "Orchestrate evaluated RAG and GraphRAG with Laya decisions. Use for RAG or GraphRAG with Laya. Do NOT use for standalone graph drawing."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 0.1.0
  owner_agent: codenavi-agent
---

# rag-laya-expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Outcome
Compose rag-expert, ragraph-expert and laya-expert into one measured local evidence/training workflow.

## Workflow
1. Read briefing/continuity and inspect actual service/model/graph health; load only the sibling skill needed by the current step.
2. Acquire/analyze official sources in bounded parallel tasks; preserve source/license/revision/hash and separate discovery from acquired knowledge.
3. Establish hybrid RAG baseline, build the incremental graph and publish committed changes to the live panel.
4. Apply Laya to bounded strategy/relevance decisions; retain deterministic hybrid fallback for uncalibrated or low-confidence predictions.
5. Prepare disjoint domain datasets with human test review; run Laya RLCD and LLM QLoRA as separate sequential GPU experiments.
6. Compare hybrid, graph and Laya-assisted behavior on identical questions; retain sources, metrics, review status and rollback/base checkpoints.

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

## Composition
- Read [rag-expert](../rag-expert/SKILL.md) for evidence retrieval and grounding.
- Read [ragraph-expert](../ragraph-expert/SKILL.md) for graph ingestion/retrieval/visualization.
- Read [laya-expert](../laya-expert/SKILL.md) for typed decisions, RLCD and calibration.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
