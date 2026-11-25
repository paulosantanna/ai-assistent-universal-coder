---
name: tao-finetune-huggingface-model
description: "Fine-tune a Hugging Face model with TAO. Use for tao finetune. Do NOT use for Megatron training."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "0.1.0"
  owner_agent: codenavi-agent
---

# TAO Hugging Face Fine-tune

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/tao-finetune-huggingface-model`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Fine-tune one Hugging Face model through the TAO workflow, with host and Docker gaps named instead of invented.

## Workflow

1. Inspect the model id and dataset the user is allowed to train on.
2. If the GPU host or Docker contract depends on a TAO platform skill that is not installed, name it and stop.
3. Research the recipe, then generate the project and smoke-test only after confirmation.
4. Train, evaluate, and infer with the procedure's error playbook.
5. Push to a hub only when the user asks, and never print tokens.

## Inputs, outputs, and stop

Inputs: model id, authorized dataset, and TAO host
Outputs: project, metrics that were run, and any missing platform skill
Stop when a required tool, permission, or evidence check fails. Do not start training or push weights without confirmation. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
