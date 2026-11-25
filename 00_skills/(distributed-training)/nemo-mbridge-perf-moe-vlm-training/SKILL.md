---
name: nemo-mbridge-perf-moe-vlm-training
description: "Train multimodal MoE VLMs in Megatron Bridge. Use for moe vlm training. Do NOT use for text-only dense models."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# MoE VLM Training

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/nemo-mbridge-perf-moe-vlm-training`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Choose FSDP or 3D parallel for a MoE vision-language model and record the data mode.

## Workflow

1. Confirm the model is a MoE VLM and whether data is mock or real.
2. Choose FSDP or 3D parallel using the decision guide, not a single hardware anecdote.
3. Keep vision and language batch constraints from the procedure.
4. Show the launch and wait for confirmation.
5. Report which findings were rechecked in the checkout.

## Inputs, outputs, and stop

Inputs: VLM MoE config, data mode, and GPU topology
Outputs: strategy choice and launch evidence or the unrun command
Stop when a required tool, permission, or evidence check fails. Do not apply a text-only dense recipe unchanged. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
