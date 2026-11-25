---
name: digital-health-clinical-asr-finetune
description: "Fine-tune Parakeet when KER stays high. Use for clinical asr finetune. Do NOT use for setup."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# Clinical ASR Fine-tune

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/digital-health-clinical-asr-finetune`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Run stock NeMo SFT on Parakeet TDT v2 only after a KER gate and an explicit GPU cost confirmation.

## Workflow

1. Require a prior eval whose priority KER is above the procedure threshold.
2. Ask for GPU cost confirmation. Do not auto-answer.
3. Split train and validation with the term-aware method.
4. Run stock SFT, then the offline next-cycle eval.
5. Deploy to Riva only if the user asks in a separate confirmation.

## Inputs, outputs, and stop

Inputs: scored manifest, base model, and confirmed GPU budget
Outputs: checkpoint path and the follow-up eval status
Stop when a required tool, permission, or evidence check fails. Stop when KER evidence or cost confirmation is missing. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
