---
name: llm-model-selection-expert
description: "Select the best current model for a workload, using live capability data and evals. Use for model selection. Do NOT use for unrelated stacks."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# LLM Model Selection Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Select the best current model/model-family for a concrete workload using live authoritative capability information plus project evals.

## Procedure
Define workload/safety/latency/cost/context/tooling/privacy constraints → enumerate currently available candidates from official provider/model docs → normalize harness → run representative eval set → compare quality, tool reliability, structured output, latency, throughput and cost → choose primary/fallback → document date/version and retirement trigger.

Never encode 'latest/best model' as permanent knowledge. Model availability and fine-tuning/tool support are freshness-sensitive.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
