---
name: nemo-mbridge-perf-cuda-graphs
description: "Enable CUDA graphs in Megatron Bridge. Use for cuda graphs, graph capture, or TE. Do NOT use for Slurm setup."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# CUDA Graphs

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/nemo-mbridge-perf-cuda-graphs`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Enable a CUDA graph mode that satisfies the TE and RNG constraints in the checkout.

## Workflow

1. Choose local full-iteration or TE scoped capture from the model type.
2. Check RNG tracker, warmup, and delayed-wgrad interactions in the procedure.
3. Reject the mode when CPU offload or another listed incompatibility is on.
4. Capture only after warmup, then run the smoke check or return it unrun.
5. Report success only against the procedure's success criteria and a real log.

## Inputs, outputs, and stop

Inputs: training config, GPU availability, and TE version
Outputs: graph config and smoke evidence
Stop when a required tool, permission, or evidence check fails. Do not enable graphs on an incompatible offload or MoE setting. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
