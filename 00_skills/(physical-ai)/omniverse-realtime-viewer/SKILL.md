---
name: omniverse-realtime-viewer
description: "Route an Omniverse realtime viewer change. Use for realtime viewer, XR, or USD streaming. Do NOT use for CAD conversion."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "0.3.0"
  owner_agent: codenavi-agent
---

# Omniverse Realtime Viewer

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/omniverse-realtime-viewer`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Route a realtime viewer change to the reference that owns that feature and follow only that contract.

## Workflow

1. Name the app surface: streaming, XR, viewport, CAE, or solid modeling.
2. Open the one upstream module for that surface. Do not load the whole corpus.
3. Prefer the upstream solid-modeling path the procedure names before a local workaround.
4. Change only the feature the user asked for.
5. Validate with the module's check, or report that the tool was not available.

## Inputs, outputs, and stop

Inputs: viewer app checkout and the feature to change
Outputs: the edit or the exact unrun validation
Stop when a required tool, permission, or evidence check fails. Do not convert CAD in this skill. Use omniverse-cad-to-simready. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
