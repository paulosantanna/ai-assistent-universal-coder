# JUDGE_ENGINE.md

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

Independently evaluate whether work is acceptable.

## Judge types

- Architecture Judge
- Implementation Judge
- Security Judge
- Testing Judge
- Performance Judge
- Documentation Judge
- Governance Judge
- Clinical Judge when applicable

## Judge output

```json
{
  "judge": "string",
  "decision": "accept|reject|block|needs_rework",
  "score": 0.0,
  "deductions": [],
  "missing_evidence": [],
  "risks": [],
  "required_rework": []
}
```

## Rule

Judges must not be optimistic without evidence.
