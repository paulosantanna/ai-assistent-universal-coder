---
name: nemo-mbridge-perf-sequence-packing
description: "Pack sequences for long-context training. Use for sequence packing or packed data. Do NOT use for CPU offload."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# Sequence Packing

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/nemo-mbridge-perf-sequence-packing`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Enable a packing path that matches the data type and the context-parallel constraints.

## Workflow

1. Choose offline LLM packing, collate-time VLM packing, or Energon online packing from the data format.
2. Read the pack length and CP constraints before editing the config.
3. Keep attention masks and loss weights consistent with the unpacked objective.
4. Run the verification the procedure names, or return it unrun.
5. Do not combine packing with a constraint the pitfalls list forbids.

## Inputs, outputs, and stop

Inputs: dataset format, sequence length, and CP setting
Outputs: packing config and verification status
Stop when a required tool, permission, or evidence check fails. Stop when the data loader does not match any documented packing path. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
