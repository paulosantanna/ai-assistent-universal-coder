---
name: nemo-mbridge-resiliency
description: "Add fault tolerance and restart to Bridge. Use for training resiliency or stragglers. Do NOT use for lint."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# Training Resiliency

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/nemo-mbridge-resiliency`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Enable one resiliency feature with its launcher and a verification check.

## Workflow

1. Name the failure: fault, straggler, preemption, or restart.
2. Prefer the NeMo Run plugin on Slurm when the procedure recommends it.
3. Keep experimental in-process restart and the re-run state machine labeled experimental.
4. Confirm before changing a live job's launcher.
5. Verify with the check for that feature or report it unrun.

## Inputs, outputs, and stop

Inputs: cluster type, failure mode, and current launcher
Outputs: one resiliency config and its verification status
Stop when a required tool, permission, or evidence check fails. Do not enable every resiliency feature at once. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
