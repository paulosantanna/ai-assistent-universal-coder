---
name: nemo-mbridge-perf-memory-tuning
description: "Tune Megatron Bridge memory before speed. Use for memory tuning, OOM, or recompute. Do NOT use for CUDA graphs."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# Memory Tuning

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/nemo-mbridge-perf-memory-tuning`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Relieve an out-of-memory failure with the first compatible memory lever, then measure.

## Workflow

1. Confirm the OOM stage and the current parallelism.
2. Try expandable segments and parallelism resizing before activation recompute.
3. Use CPU offload only when the CPU-offload skill's constraints are met.
4. Treat upstream strategy tables as unrerun until this job measures them.
5. Verify the run allocates and steps once, or return that command unrun.

## Inputs, outputs, and stop

Inputs: OOM log, config, and GPU memory
Outputs: one memory change and the allocation result
Stop when a required tool, permission, or evidence check fails. Do not stack recompute, offload, and a parallelism change in one unverified edit. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
