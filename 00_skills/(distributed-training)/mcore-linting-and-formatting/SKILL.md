---
name: mcore-linting-and-formatting
description: "Lint and format Megatron-LM before a PR. Use for mcore lint, autoformat.sh, or ruff. Do NOT use for training."
license: "Apache-2.0"
metadata:
  author: NVIDIA Corporation
  version: "1.0.0"
  owner_agent: codenavi-agent
---

# Megatron-LM Lint

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

Provenance: adapted from NVIDIA/skills `e34173c2efbe` `skills/mcore-linting-and-formatting`. This is not an NVIDIA-verified byte copy. Read [provenance](references/provenance.md).

## Outcome

Format and lint a Megatron-LM checkout with its own autoformat.sh and import order.

## Workflow

1. Confirm the current repo is Megatron-LM and tools/autoformat.sh exists.
2. Run check mode before fix mode.
3. Run isort on edited Python files and keep the 119-character project limit.
4. Install the linting group only if the user asks.
5. Report the tool output. Do not claim CI passed unless CI ran.

## Inputs, outputs, and stop

Inputs: Megatron-LM checkout and the files changed
Outputs: formatter output and remaining violations
Stop when a required tool, permission, or evidence check fails. Stop if autoformat.sh is absent. Do not invent a different linter config. Never invent commands, image tags, metrics, or clinical findings.

## Modules

- Read [procedure](references/procedure.md) before any command, config edit, or deployment.
- Read [examples](references/examples.md) when choosing an invocation or a boundary.
- Read [defects](references/defects.md) before trusting an upstream benchmark, version, or sibling skill.
- Read [provenance](references/provenance.md) when citing license, commit, or what was not copied.
- Open `references/upstream/` only for the mode the procedure names.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
