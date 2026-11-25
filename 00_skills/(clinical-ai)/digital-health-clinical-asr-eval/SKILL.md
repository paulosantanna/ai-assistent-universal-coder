---
name: digital-health-clinical-asr-eval
description: "Score a clinical ASR manifest with KER. Use for clinical asr eval or a score. Do NOT use for fine-tuning."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.1.0"
  owner_agent: codenavi-agent
---

# Clinical ASR Eval

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/digital-health-clinical-asr-eval`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Score a NeMo clinical manifest and publish a KER breakdown without calling it a clinical validation.

## Workflow

1. Disclose that audio may be sent to the chosen ASR NIM.
2. Pick the NIM and transcribe with the procedure's command.
3. Score the four metrics and build the five-section leaderboard.
4. Label KER by IPA source as diagnostic of the benchmark, not of a patient.
5. If priority KER stays above the procedure's fine-tune threshold, name the fine-tune skill instead of starting it.

## Inputs, outputs, and stop

Inputs: manifest, chosen ASR NIM, and permission to send audio
Outputs: score table and the decision to stop or hand off
Stop when a required tool, permission, or evidence check fails. Do not start a fine-tune from this skill. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
