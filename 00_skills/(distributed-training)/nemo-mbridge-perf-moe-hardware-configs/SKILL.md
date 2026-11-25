---
name: nemo-mbridge-perf-moe-hardware-configs
description: "Seed MoE configs from a hardware playbook. Use for moe hardware configs or H100. Do NOT use as measured proof."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# MoE Hardware Configs

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/nemo-mbridge-perf-moe-hardware-configs`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Pick a hardware playbook as a seed config, then mark every figure as unverified until rerun.

## Workflow

1. Match model family and GPU generation to one playbook.
2. Copy only the config keys, and label the performance band as upstream and stale until measured.
3. Re-read PP, recompute, and environment keys in the checkout.
4. Hand a live tune to nemo-mbridge-perf-moe-optimization-workflow.
5. Do not treat the seed as a benchmark result.

## Inputs, outputs, and stop

Inputs: model family and GPU generation
Outputs: seed config with an explicit unverified label
Stop when a required tool, permission, or evidence check fails. Stop if the model family is not in the playbook. Do not interpolate a new one silently. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
