---
name: nemo-mbridge-perf-moe-optimization-workflow
description: "Optimize MoE training from measured evidence. Use for moe optimization workflow. Do NOT use for hardware seed tables."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# MoE Optimization Workflow

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/nemo-mbridge-perf-moe-optimization-workflow`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Walk a MoE run from a frozen measurement contract through one evidence-backed change.

## Workflow

1. Freeze batch, sequence, precision, and the metric before changing flags.
2. Make the run memory-feasible before tuning speed.
3. Profile the dominant bottleneck and change one factor.
4. Re-measure against the frozen contract.
5. Send hardware starting points to nemo-mbridge-perf-moe-hardware-configs and dispatcher choice to the dispatcher skill.

## Inputs, outputs, and stop

Inputs: a real run config and permission to profile
Outputs: one change with before and after evidence, or the profile command unrun
Stop when a required tool, permission, or evidence check fails. Do not stack unmeasured flags. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
