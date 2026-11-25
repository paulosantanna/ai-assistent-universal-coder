---
name: nemo-mbridge-perf-parallelism-strategies
description: "Choose Megatron Bridge parallelism. Use for parallelism strategies or TP DP PP. Do NOT use for lint."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# Parallelism Strategies

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/nemo-mbridge-perf-parallelism-strategies`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Select a TP, DP, PP, CP, or EP combination that fits the model and the GPU topology.

## Workflow

1. Read model class, parameter count, sequence length, and GPU topology.
2. Apply the minimum GPU and memory rules in the procedure.
3. Reject a combination the pitfalls section marks invalid.
4. Write the config and the verification command.
5. Wait for confirmation before launching.

## Inputs, outputs, and stop

Inputs: model shape and hardware topology
Outputs: parallelism plan and the config diff
Stop when a required tool, permission, or evidence check fails. Do not present a plan as a measured throughput. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
