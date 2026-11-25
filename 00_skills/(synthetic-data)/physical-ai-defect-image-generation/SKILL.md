---
name: physical-ai-defect-image-generation
description: "Generate inspection defect images. Use for defect image generation. Do NOT use for clinical scans."
license: "CC-BY-4.0 AND Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.1"
  owner_agent: codenavi-agent
---

# Defect Image Generation

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/physical-ai-defect-image-generation`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Generate synthetic defect images for an inspection model using a named cookbook and confirmed GPU job.

## Workflow

1. Map the defect class to a cookbook. Do not invent a crop knob the flow does not have.
2. Run preflight order from the procedure after the first-time gate.
3. Confirm GPU size and credentials handling before submit.
4. Monitor the job and render outputs with the procedure's retrieval steps.
5. Report the chosen knobs and any step that did not run.

## Inputs, outputs, and stop

Inputs: defect class, authorized background images, and cluster access
Outputs: generated images, config used, and job evidence
Stop when a required tool, permission, or evidence check fails. Do not generate clinical or identifiable imagery. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
