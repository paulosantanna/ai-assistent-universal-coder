---
name: rollback-planner
description: "Generate rollback plans that define how to undo every operation safely. Use for rollback planning. Do NOT use for unapproved production changes."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Rollback Planner Skill

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

**ID:** rollback-planner
**Version:** 1.0.0
**Owner Agent:** codenavi-agent
**Risk Level:** low

## Mission
Generate rollback plans for proposed changes — defining exactly how to undo every operation safely.

## Scope
- Analyze proposed changes from patch
- Define undo operations for each change
- Generate rollback-plan.md with verification steps

## Allowed Actions
- `filesystem.read` — read patch files
- `filesystem.write_aeos` — write rollback plan to .aeos/patches/{execution_id}/
- `generate_evidence` — register rollback plan

## Forbidden Actions
- Execute any rollback operation
- Modify real files as part of planning
- Delete any real files

## Required Capabilities
- READ_REPOSITORY
- PLAN_ROLLBACK
- GENERATE_REPORT

## Required Evidence
- Patch files read (SHA-256)
- Rollback plan generated (SHA-256)
- Verification steps documented

## Prompt Contract

- State the objective, target scope, assumptions and constraints before execution.
- Use only evidence-backed facts; mark uncertainty explicitly.
- Route tool access through approved command, MCP or Tool Router paths.
- Redact secrets, credentials, tokens and sensitive values.
- Return facts, assumptions, risks, recommendations, evidence_refs and blocking_conditions when applicable.
- Stop when required evidence, permissions, policy approval or input context is missing.

## Quality Gates
- Every proposed change must have a corresponding undo operation
- Rollback must include verification steps
- Rollback plan must be actionable

## Output Schema
```json
{
  "strategy": "restore_originals + delete_generated",
  "operations": [
    {"operation": "restore", "target": "src/service.py", "method": "git checkout -- src/service.py"},
    {"operation": "delete", "target": ".aeos/patches/ex-123/proposed.patch", "method": "rm"},
    {"operation": "verify", "target": "", "method": "git diff --stat && run tests"}
  ],
  "rollback_conditions": ["regression", "test_failure", "approval_revoked"]
}
```

## Blocking Conditions
- Any change without undo operation
- Rollback plan is empty
- Verification step is missing

## Examples of Allowed Behavior
- Create rollback-plan.md for a patch that modifies src/service.py
- Define git checkout commands for each modified file

## Examples of Forbidden Behavior
- Executing the rollback plan
- Modifying source files as part of planning

Provenance: [provenance](references/provenance.md).

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
