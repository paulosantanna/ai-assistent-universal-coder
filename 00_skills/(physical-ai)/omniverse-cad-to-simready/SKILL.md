---
name: omniverse-cad-to-simready
description: "Turn CAD into a SimReady USD package. Use for cad to simready or prop packaging. Do NOT use for NuRec."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "0.2.0"
  owner_agent: codenavi-agent
---

# CAD to SimReady

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/omniverse-cad-to-simready`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Convert an authorized CAD or source asset into a SimReady USD package and report the validation result.

## Workflow

1. Confirm the asset path, units, and that the request is packaging rather than neural reconstruction.
2. Run the preflight and conversion steps in the order the procedure gives.
3. Assemble the package layout from the publishing notes.
4. Validate the USD. If the Omniverse tools are absent, return the commands unrun.
5. Do not claim SimReady compliance without the validator output.

## Inputs, outputs, and stop

Inputs: authorized CAD or mesh and the Omniverse tool install
Outputs: package path and validation evidence
Stop when a required tool, permission, or evidence check fails. Stop when a required converter or validator is missing. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
