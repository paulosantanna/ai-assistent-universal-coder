---
name: vss-summarize-video
description: "Summarize a video on an authorized VSS deployment. Use for vss summarize. Do NOT use for archive search."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "3.3.0"
  owner_agent: codenavi-agent
---

# VSS Summarize Video

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/vss-summarize-video`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Summarize one recording through the vss CLI on a deployment the user already operates.

## Workflow

1. Confirm the deployment, the recording, and that the user may send it to that VSS.
2. Select the backend and prepare the video with the procedure's VIOS steps.
3. Collect LVS settings and submit once through the CLI.
4. Use the documented VLM fallback only when the primary path fails.
5. Return the summary with the command and any stage that did not run.

## Inputs, outputs, and stop

Inputs: authorized VSS deployment and the recording identity
Outputs: summary text and the CLI evidence
Stop when a required tool, permission, or evidence check fails. Do not fall back to an undocumented private API or another person's video. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
