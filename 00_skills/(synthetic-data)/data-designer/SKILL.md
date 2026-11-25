---
name: data-designer
description: "Build a synthetic dataset with Data Designer. Use for synthetic data or a data-designer pipeline. Do NOT use for real PHI."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# Data Designer

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/data-designer`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Produce a Data Designer config script for the dataset the user described, after checking the workspace.

## Workflow

1. Read the user dataset description and search the workspace for an existing matching script.
2. Use interactive mode unless the user asked for an opinionated build.
3. Read person-sampling or seed-dataset notes only when the request needs them.
4. Write a load_config_builder script with PEP 723 metadata. Do not install data-designer without permission.
5. Preview only after the user allows network access.

## Inputs, outputs, and stop

Inputs: dataset description and any seed file the user explicitly supplied
Outputs: Python config script and the preview status
Stop when a required tool, permission, or evidence check fails. Do not drop output columns unless the user asks or the column exists only to derive others. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
