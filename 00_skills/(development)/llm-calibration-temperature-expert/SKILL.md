---
name: llm-calibration-temperature-expert
description: "Engineer LLM decoding and calibration behavior instead of tuning temperature blindly. Use for LLM calibration. Do NOT use for unrelated stacks."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# LLM Calibration & Temperature Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Engineer and evaluate decoding/calibration behavior for LLM applications instead of treating temperature as a magic quality knob.

## Coverage
Temperature, top-p/top-k when supported, deterministic/seeded runs when supported, reasoning-effort controls, log-probability/confidence signals where available, structured-output reliability, sampling diversity, self-consistency, uncertainty calibration and abstention thresholds.

## Procedure
1. Define task and error cost.
2. Establish model/prompt/harness baseline.
3. Determine which decoding controls the selected provider/model actually supports from current official docs.
4. Create representative eval slices.
5. Change one sampling/reasoning variable at a time.
6. Measure correctness, variance, format compliance, refusal/abstention behavior, latency and cost.
7. Choose production settings by evidence, not folklore.
8. Lock settings and regression evals by model/version.

## Rules
- `temperature=0` is not proof of universal determinism.
- Never compare models under materially different harnesses without documenting it.
- Recalibrate when model/version/prompt/tool context changes.
- For high-stakes outputs, confidence must come from task-specific eval evidence, not the model's verbal certainty.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
