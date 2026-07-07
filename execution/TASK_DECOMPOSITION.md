# TASK_DECOMPOSITION.md

> **AEOS Chief/Staff Edition**
>
> This document is part of the AI Engineering Operating System.
> It is designed for AI agents acting as Chief AI Architect, Chief Software Architect,
> Principal Engineer, Staff Software Engineer and Staff AI Engineer.
>
> Core invariants:
> - Evidence before claims.
> - Architecture before implementation.
> - Delegation before context bloat.
> - Verification before completion.
> - Knowledge persistence after every material outcome.
> - Human authority over unsafe or high-impact decisions.


## Purpose

Break complex work into independent work packages.

## Work package schema

```json
{
  "task_id": "string",
  "title": "string",
  "objective": "string",
  "owner_role": "string",
  "inputs": [],
  "outputs": [],
  "dependencies": [],
  "risk_level": "low|medium|high|critical",
  "allowed_actions": [],
  "forbidden_actions": [],
  "evidence_required": [],
  "completion_criteria": [],
  "verification_commands": []
}
```

## Decomposition rules

- Each task has one primary objective.
- Each task has one owner role.
- Each task has explicit inputs and outputs.
- Each task has measurable completion criteria.
- Shared mutable files require coordination.
- Architecture-impacting tasks require council review.

## Dependency types

- data dependency;
- code dependency;
- architecture dependency;
- test dependency;
- security dependency;
- deployment dependency;
- knowledge dependency.

## Granularity

Tasks are too large when:
- one specialist cannot own them;
- evidence requirements are unclear;
- test strategy is mixed;
- implementation and review are combined;
- architecture and coding are combined.

Tasks are too small when:
- overhead exceeds value;
- output cannot be independently validated;
- task has no meaningful completion criterion.

## Output rule

Every decomposed task must be executable without requiring hidden context.
