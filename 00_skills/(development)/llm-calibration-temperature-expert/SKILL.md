---
name: llm-calibration-temperature-expert
description: Engineer and evaluate decoding/calibration behavior for LLM applications instead of treating temperature as a magic quality knob. Use when the user requests llm calibration temperature expert or invokes llm-calibration-temperature-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# LLM Calibration & Temperature Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi v1

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

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
