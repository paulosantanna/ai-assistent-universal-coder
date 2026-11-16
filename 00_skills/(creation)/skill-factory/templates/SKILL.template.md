---
name: {{slug}}
description: "{{description}}"
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# {{title}}

Governance: CodENavi Full Workspace v2; skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission

{{mission}}

## Workflow

1. Confirm scope, inputs and permissions; stop when any is missing.
2. Gather evidence from the authorized target only.
3. Execute the bounded procedure.
4. Verify against the acceptance checks; never claim an unexecuted check passed.

## Inputs and outputs

- Inputs: {{inputs}}
- Outputs: {{outputs}}

## Verification

- {{acceptance_checks}}

## Stop conditions

- Scope must expand, approval is required, evidence cannot be produced, or a critical blocker remains.

## Modules

- Read [{{module}}](references/{{module}}.md) only {{load_condition}}.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
