---
name: nemo-automodel-distributed-training
description: "Configure NeMo AutoModel distributed training. Use for automodel FSDP or tensor parallel. Do NOT use for lint-only."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# NeMo AutoModel Training

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/nemo-automodel-distributed-training`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Choose and configure FSDP2, TP, PP, CP, or MoE parallelism for an AutoModel run the user confirms.

## Workflow

1. Read model size, GPU count, topology, and sequence length from the user project.
2. Select a strategy from the procedure's sizing rules. Do not mix constraints the text marks incompatible.
3. Write the YAML or API change in the project, not a new sample repo.
4. Show the launch command and wait for confirmation before a multi-GPU run.
5. Report the strategy, the world size, and whether the launch ran.

## Inputs, outputs, and stop

Inputs: model config, GPU topology, and authorization to spend GPU time
Outputs: parallelism config and launch evidence or the unrun command
Stop when a required tool, permission, or evidence check fails. Do not start a shared-cluster job without confirmation. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
