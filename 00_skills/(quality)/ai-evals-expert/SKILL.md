---
name: ai-evals-expert
description: "Turn AI quality claims into reproducible eval evidence. Use for AI quality evaluation. Do NOT use as deployment approval or for unexecuted checks."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# AI Evals Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Turn AI quality claims into reproducible evaluation evidence.

## Framework
SPECIFY → MEASURE → IMPROVE.

Define task claim, golden set, failure taxonomy, slices/edge cases, harness, model/reasoning/tool configuration, budgets and scoring. Use deterministic graders where possible; LLM graders require calibration and human audit. Test contamination, reward hacking, broken tasks, refusals and harness artifacts. Maintain regression gates for quality, safety, latency and cost.

Never report a single aggregate score without describing what it measures and the tested system configuration.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
