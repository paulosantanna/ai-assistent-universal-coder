---
name: dali-dynamic-mode
description: "Write DALI dynamic-mode pipelines in ndd. Use for dali dynamic mode or ndd. Do NOT use for static pipeline-only edits."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# DALI Dynamic Mode

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/dali-dynamic-mode`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Implement or migrate a DALI pipeline in experimental dynamic mode without changing pipeline-only code by habit.

## Workflow

1. Confirm the task touches nvidia.dali.experimental.dynamic or an ndd migration.
2. Use Tensor and Batch types from the procedure and keep device placement explicit.
3. Set RNG seeds deliberately when the sample order must be reproducible.
4. Migrate pipeline mode only with the procedure's mistake list in view.
5. Run a small batch and report shapes, devices, and any operator the installed DALI lacks.

## Inputs, outputs, and stop

Inputs: pipeline intent, installed DALI version, and sample input
Outputs: dynamic-mode code and the batch check that ran
Stop when a required tool, permission, or evidence check fails. Stop if the installed DALI has no experimental.dynamic module. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
