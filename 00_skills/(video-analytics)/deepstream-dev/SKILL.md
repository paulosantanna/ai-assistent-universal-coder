---
name: deepstream-dev
description: "Build DeepStream pipelines with pyservicemaker. Use for deepstream or GStreamer inference. Do NOT use for VSS search."
license: "CC-BY-4.0 AND Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.1.1"
  owner_agent: codenavi-agent
---

# DeepStream

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/deepstream-dev`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Build or debug a DeepStream pipeline against the installed SDK, using the reference that matches the failing stage.

## Workflow

1. Confirm the DeepStream SDK version and whether the task is inference, tracking, message, or a pipeline bug.
2. Read only the reference for that stage before editing config or Python.
3. Keep buffer ownership and element caps as the reference states them.
4. Run the smallest pipeline check the user authorizes.
5. Report the SDK version, the config changed, and the log evidence.

## Inputs, outputs, and stop

Inputs: DeepStream SDK install, pipeline goal, and authorized media
Outputs: pipeline change and the runtime evidence, or the unrun command
Stop when a required tool, permission, or evidence check fails. Do not point a pipeline at a camera or stream the user does not control. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
