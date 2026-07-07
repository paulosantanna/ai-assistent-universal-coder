# FAILURE_PREDICTION.md

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

Predict failures before implementation.

## Failure classes

- correctness failure;
- architecture regression;
- dependency breakage;
- data corruption;
- security vulnerability;
- performance regression;
- observability blind spot;
- test fragility;
- deployment failure;
- governance failure;
- user safety failure.

## Pre-change questions

- Who depends on this?
- What tests cover this?
- What happens if it fails?
- Can it be rolled back?
- What is the blast radius?
- What hidden state exists?
- What external services are involved?
- What sensitive data is touched?

## Failure prediction output

```json
{
  "predicted_failures": [],
  "blast_radius": "string",
  "mitigations": [],
  "required_tests": [],
  "rollback_plan": "string"
}
```

## Rule

High-impact failure risk requires mitigation before implementation.
