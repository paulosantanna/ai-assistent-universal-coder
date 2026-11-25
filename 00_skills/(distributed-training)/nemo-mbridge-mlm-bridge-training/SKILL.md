---
name: nemo-mbridge-mlm-bridge-training
description: "Run Megatron-LM and Bridge correlation training. Use for mlm bridge training. Do NOT use for lint."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# MLM and Bridge Training

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/nemo-mbridge-mlm-bridge-training`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Run a paired Megatron-LM and Megatron Bridge correlation check, or return the commands unrun.

## Workflow

1. Confirm the Bridge checkout and whether the data is mock or real.
2. Use the 2-layer correlation pair before a multi-GPU recipe.
3. Compare the losses the procedure names. Do not call them matched without both logs.
4. Switch the Megatron-Core submodule only when the user asks, and record the commit.
5. Hand style fixes to mcore-linting-and-formatting.

## Inputs, outputs, and stop

Inputs: Megatron Bridge checkout and the recipe or mock config
Outputs: both command logs or the unrun pair
Stop when a required tool, permission, or evidence check fails. Do not claim correlation from a single side's log. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
