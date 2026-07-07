# CHECKPOINT_ENGINE.md

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

Preserve state, prevent context loss and enable deterministic recovery.

## Checkpoint triggers

- session start;
- before repository mutation;
- before delegation;
- after milestone;
- after failed test;
- after rejected judge review;
- after significant decision;
- at context threshold;
- before final response.

## Checkpoint schema

```json
{
  "checkpoint_id": "uuid",
  "timestamp": "iso-8601",
  "trigger": "string",
  "objective": "string",
  "phase": "string",
  "completed_tasks": [],
  "pending_tasks": [],
  "decisions": [],
  "evidence": [],
  "risks": [],
  "blockers": [],
  "next_action": "string",
  "resume_instructions": "string"
}
```

## Recovery protocol

1. Load latest valid checkpoint.
2. Validate objective.
3. Validate completed tasks.
4. Re-check stale evidence.
5. Resume at next action.
6. Do not repeat completed work unless evidence is invalid.

## Checkpoint quality

A checkpoint is valid only if another agent can resume from it without guessing.

## Anti-patterns

Invalid checkpoints:
- vague summaries;
- missing next action;
- missing evidence;
- missing blockers;
- no task IDs;
- no decision history.
