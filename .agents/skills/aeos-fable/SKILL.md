---
name: aeos-fable
description: Standard problem-solving loop for AEOS (classify ask, define done, gather evidence, decide, act surgically, verify by observation, report outcome-first).
---

# Enterprise Skill: aeos-fable

## Mission

Provide enterprise-grade Fable Method problem-solving loop capability inside AEOS v1.1.

## Production Scope

This skill governs multi-step problem solving across coding, devops, research, data analysis, business operations, finance, legal compliance, and design/UX inside AEOS system workflows.

## Allowed Actions

- Read authorized workspace files, specs, and configurations through Tool Router.
- Perform bounded parallel research (web, documentation, source code).
- Execute local non-destructive verification commands (tests, builds, lints, dry-runs).
- Generate reports, plans, audit summaries, and candidate lessons.
- Route domain-specific tasks to domain adapters (`references/domains/`).

## Forbidden Actions

- Direct un-routed tool execution or filesystem bypass.
- Secret, key, or credential reading/exposure.
- Unauthorized outward or irreversible actions (commits, pushes, deploys, deletes, payments) without explicit user authorization quotes.
- Verification theater (claiming tests passed without running them or inspecting output).
- Silent step-dropping or scope expansion beyond declared boundaries.
- Fabricating data, API signatures, endpoints, or evidence from memory.

## Required Inputs

```yaml
input:
  task_or_ask: "The core problem, question, or change request"
  mode: "full (default) | plan | audit | report"
  domain: "coding (default) | devops | research | data-analysis | business-ops | finance | legal-compliance | design-ux | marketing"
  evidence_refs: []
```

## Required Output Schema

```json
{
  "skill_id": "aeos-fable",
  "status": "PASS|BLOCKED|REVIEW",
  "shape": "task|assessment|plan-first",
  "facts": [],
  "assumptions": [],
  "risks": [],
  "recommendations": [],
  "evidence_refs": [],
  "verifications": {
    "done_criterion": "",
    "surrounding_system_healthy": true,
    "twins_searched": ""
  },
  "gates": {
    "intent_line": "",
    "auth_line": "",
    "pending_line": "",
    "twins_line": ""
  },
  "blocking_conditions": []
}
```

## Prompt Contract

- State the objective, target scope, assumptions, and constraints before execution.
- Classify the ask shape (Question/Assessment, Task, Plan-first) before taking any action.
- Enforce the Triviality Gate and Fit Gate.
- Gather primary sources before modifying any behavior.
- Execute smallest correct changes with Intent Gate verification.
- Verify both target criteria and surrounding system health by direct observation.
- Report outcome-first with zero step headers or method scaffolding.

## Quality Gates

- Facts cite concrete evidence (`file:line`, command output, or fetched URL).
- Assumptions are explicit and checkable.
- Risks are classified with severity.
- Intent line (`INTENT:`) present whenever code/behavior changed.
- Auth line (`AUTH:`) present whenever outward/irreversible action was taken.
- Twins line (`TWINS:`) present whenever a defect fix was applied.
- Pending line (`PENDING:`) present when documented follow-up was deferred.

## Stop Conditions

- 3 consecutive failed fix-verify cycles on the same issue.
- Missing required human authorization for outward/irreversible actions.
- Unreachable primary evidence when inference alone is unsafe.
- Secret/credential exposure detected.

---

# The Fable Method Loop

Follow the exact Fable Method loop as specified in `fable/SKILL.md`.
Refer to `references/failure-modes.md`, `references/examples.md`, `references/flowcharts.md`, and `references/domains/`.
