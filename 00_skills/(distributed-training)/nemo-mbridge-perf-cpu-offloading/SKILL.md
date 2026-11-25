---
name: nemo-mbridge-perf-cpu-offloading
description: "Offload optimizer or activations to CPU. Use for cpu offloading. Do NOT use for CUDA graphs."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# CPU Offloading

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/nemo-mbridge-perf-cpu-offloading`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Enable a documented CPU offload path that is compatible with the rest of the run.

## Workflow

1. Choose optimizer offload for large models or activation offload only where the procedure allows it.
2. Reject combinations marked incompatible with CUDA graphs or fine-grained offload.
3. Edit the config keys the reference lists.
4. Run the unit or smoke check, or return it unrun.
5. Record the memory effect only if it was measured.

## Inputs, outputs, and stop

Inputs: current training config and the memory symptom
Outputs: offload config and compatibility check
Stop when a required tool, permission, or evidence check fails. Do not enable offload together with a forbidden CUDA graph setting. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
