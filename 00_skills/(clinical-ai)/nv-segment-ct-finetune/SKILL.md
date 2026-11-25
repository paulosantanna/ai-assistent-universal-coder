---
name: nv-segment-ct-finetune
description: "Fine-tune NV-Segment-CT VISTA3D on NIfTI. Use for ct segmentation finetune. Do NOT use for MRI generation."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# NV-Segment CT Fine-tune

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/nv-segment-ct-finetune`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Fine-tune NV-Segment-CT on paired CT image and label NIfTI with checkpoint evidence.

## Workflow

1. Choose standard or fixed-channel softmax from the label set, not by guess.
2. Validate the datalist and keep labels out of git.
3. Confirm GPU time before launch. Optional MLflow stays local unless the user names a server.
4. Collect checkpoint and metric files the run actually wrote.
5. Do not compare to an upstream Task06 number unless that eval was rerun.

## Inputs, outputs, and stop

Inputs: authorized CT image and label datalist
Outputs: checkpoint and the metrics that were produced
Stop when a required tool, permission, or evidence check fails. Stop if labels and images do not match the data contract. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
