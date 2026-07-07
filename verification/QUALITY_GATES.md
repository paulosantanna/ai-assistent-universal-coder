# QUALITY_GATES.md

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

Define mandatory gates before completion.

## Gate classes

- build gate;
- lint gate;
- type gate;
- unit test gate;
- integration test gate;
- E2E gate;
- security gate;
- performance gate;
- observability gate;
- documentation gate;
- release gate.

## Gate record

```json
{
  "gate": "string",
  "command": "string",
  "exit_code": 0,
  "output_reference": "string",
  "status": "passed|failed|skipped",
  "skip_reason": "string"
}
```

## Rule

Skipped gates must be explicit and justified.

Unjustified skipped gate blocks completion.
