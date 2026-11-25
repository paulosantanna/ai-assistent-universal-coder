---
name: nv-generate-mr-brain-finetune
description: "Fine-tune NV-Generate MR-Brain on local NIfTI. Use for mr brain finetune. Do NOT use for CT segmentation."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# NV-Generate MR Brain Fine-tune

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/nv-generate-mr-brain-finetune`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Fine-tune NV-Generate MR-Brain on a local NIfTI datalist the user is allowed to use.

## Workflow

1. Confirm data license, de-identification, and that no file will be committed.
2. Check the datalist schema before launch.
3. Show the training command and wait for confirmation.
4. Monitor with the documented TensorBoard path if the run starts.
5. Do not approve the checkpoint for clinical or production data use.

## Inputs, outputs, and stop

Inputs: authorized NIfTI datalist and GPU confirmation
Outputs: checkpoint path and the unevaluated clinical status
Stop when a required tool, permission, or evidence check fails. Stop when identifiers are present or confirmation is missing. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
