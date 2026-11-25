---
name: nv-generate-mr-brain
description: "Generate synthetic brain MRI volumes. Use for mr brain generation. Do NOT use for clinical diagnosis."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# NV-Generate MR Brain

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/nv-generate-mr-brain`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Generate a synthetic T1, T2, FLAIR, SWI, or MRA volume with the documented runner, labeled synthetic.

## Workflow

1. Confirm the contrast and that the output is synthetic, not a patient study.
2. Read the runner flags from the procedure. The helper script was not copied into this package.
3. Use the upstream fixture contract only as a schema, not as a patient.
4. Run generation only where the model weights and GPU are already available.
5. Do not label the volume as cleared training data or as a diagnosis.

## Inputs, outputs, and stop

Inputs: contrast, output directory, and local model install
Outputs: synthetic volume path and the command status
Stop when a required tool, permission, or evidence check fails. Stop if the request is to read or diagnose a real patient scan. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
