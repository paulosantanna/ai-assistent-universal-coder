---
name: vss-ask-video
description: "Ask one question of a video on authorized VSS. Use for vss ask video. Do NOT use for archive search."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "3.3.0"
  owner_agent: codenavi-agent
---

# VSS Ask Video

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/vss-ask-video`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Answer one question about a video the user is allowed to inspect, through the configured VSS CLI.

## Workflow

1. Route summaries to vss-summarize-video and archive search to vss-search-archive.
2. Confirm the file or registered source and the sampling density the question needs.
3. Invoke the CLI once. Do not build a private HTTP call when the CLI fails.
4. Respect introspection settings from the deployment instead of guessing.
5. Return the answer, the command, and the source identity.

## Inputs, outputs, and stop

Inputs: authorized video or registered source and one question
Outputs: answer tied to the CLI result
Stop when a required tool, permission, or evidence check fails. Refuse questions that require discovering cameras or bypassing access control. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
