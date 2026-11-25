---
name: nemo-mbridge-perf-moe-dispatcher-selection
description: "Pick an MoE token dispatcher. Use for moe dispatcher, DeepEP, or alltoall. Do NOT use for parallelism sizing."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# MoE Dispatcher

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/nemo-mbridge-perf-moe-dispatcher-selection`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Choose alltoall, DeepEP, or HybridEP for the hardware and expert-parallel degree, then revalidate.

## Workflow

1. Read hardware, EP degree, and whether the backend exists in this install.
2. Apply the decision tables only as a starting choice.
3. Check the backend availability gate before naming DeepEP or HybridEP.
4. Record the choice and the verification command.
5. Send a full optimization loop to the MoE optimization workflow.

## Inputs, outputs, and stop

Inputs: hardware, EP degree, and installed dispatcher backends
Outputs: dispatcher choice and the reason it is available
Stop when a required tool, permission, or evidence check fails. Do not select a dispatcher the install does not build. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
