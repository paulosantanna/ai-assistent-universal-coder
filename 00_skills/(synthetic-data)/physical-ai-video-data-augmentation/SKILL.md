---
name: physical-ai-video-data-augmentation
description: "Augment physical-AI video on an authorized flow. Use for video augmentation or cosmos. Do NOT use for live cameras."
license: "CC-BY-4.0 AND Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# Video Data Augmentation

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/physical-ai-video-data-augmentation`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Choose and, after confirmation, run one physical-AI video augmentation flow with comparison evidence.

## Workflow

1. Disambiguate the flow from the defect class and the video the user already has rights to use.
2. Read container image and credential rules. Do not echo secrets.
3. State runtime and cost, then wait for confirmation before OSMO submit.
4. Monitor the named workflow and retrieve outputs only from that run.
5. Require a side-by-side comparison before calling an augmented clip accepted.

## Inputs, outputs, and stop

Inputs: authorized source video, flow name, and cluster access the user already holds
Outputs: run id, artifacts, and comparison evidence or the unrun submit command
Stop when a required tool, permission, or evidence check fails. Do not submit a job or use a live camera feed without confirmation. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
