---
name: physical-ai-neural-reconstruction
description: "Route NuRec reconstruction to the right step. Use for nurec or neural reconstruction. Do NOT use for SimReady."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "0.4.0"
  owner_agent: codenavi-agent
---

# Neural Reconstruction

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/physical-ai-neural-reconstruction`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Choose the NuRec workflow and name the sibling skill that owns the next step.

## Workflow

1. Classify the job: capture conversion, existing scene, indoor robot sim, edit, cleanup, benchmark, or simulator hookup.
2. Read the matching workflow letter in the upstream notes.
3. If the next step belongs to a sibling that is not installed here, name it and stop.
4. Do not download or execute that sibling unless the user asks to import it.
5. Keep secrets out of the repo and tear down only what the user names.

## Inputs, outputs, and stop

Inputs: scene or recording the user is allowed to process, and the goal
Outputs: chosen workflow and either a local step or the missing sibling name
Stop when a required tool, permission, or evidence check fails. Do not invent the steps of nurec, ncore, harmonizer, or asset-harvester. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
