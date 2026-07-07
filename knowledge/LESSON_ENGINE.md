# LESSON_ENGINE.md

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

Convert success and failure into reusable lessons.

## Lesson triggers

- failed test;
- rejected judge review;
- security finding;
- architecture correction;
- repeated bug;
- successful pattern;
- performance improvement;
- user correction;
- production incident;
- clinical/regulatory blocker.

## Lesson format

```json
{
  "lesson_id": "uuid",
  "trigger": "string",
  "problem": "string",
  "root_cause": "string",
  "what_to_do": [],
  "what_not_to_do": [],
  "evidence": [],
  "prevention": [],
  "applies_to": [],
  "status": "candidate|validated|deprecated"
}
```

## Rule

A lesson without prevention is incomplete.
