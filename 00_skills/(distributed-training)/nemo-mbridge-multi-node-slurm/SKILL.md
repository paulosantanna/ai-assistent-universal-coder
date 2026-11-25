---
name: nemo-mbridge-multi-node-slurm
description: "Turn a single-node run into a Slurm sbatch job. Use for multi-node slurm. Do NOT use for single-GPU lint."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# Multi-node Slurm

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/nemo-mbridge-multi-node-slurm`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Convert a single-node training command into a confirmed multi-node Slurm job.

## Workflow

1. Prefer the srun-native layout unless the checkout already uses torch.distributed.
2. Fill account, partition, nodes, and the container image from the user, not from a sample.
3. Show the sbatch script and wait for confirmation.
4. On failure, use the diagnosis order in the procedure before changing NCCL flags.
5. Do not delete caches unless the user names the path.

## Inputs, outputs, and stop

Inputs: working single-node command, cluster account, and container image
Outputs: sbatch script and submission evidence or the unsubmitted script
Stop when a required tool, permission, or evidence check fails. Do not sbatch without an account and an explicit confirmation. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
