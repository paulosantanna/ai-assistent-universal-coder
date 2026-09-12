---
name: tlc-plan
description: "Assimilated TLC tlc-plan 0.2.0. Turn a decided PRD, design doc, RFC or ticket into grounded tasks with observable criteria. Triggers: tlc-plan, write the task, cut this PRD into tasks, turn this design doc into work. Do not use for discovery or implementation."
---

# TLC Plan

Assimilated from installed `tlc-plan` 0.2.0 (Tech Leads Club). Original contract: `references/ORIGINAL_SKILL.md`.

## Identity

A skill of the single canonical `codenavi-agent`. It creates no new agent identity.

## Mission

Cut decided work into slices a builder can act on without guessing. Ground each slice in the repository. Write observable criteria with concrete values, surface landings and the nine-dimension sweep. Default: one task per source.

## Relationship to other skills

- Discovery / blank wish: not this skill. Use `specs`, `spec-driven` Specify, or `technical-design-doc-creator` first.
- Full specify/design/tasks feature flow: `spec-driven`.
- Obligation-first plan+checks: `spec-driven-lean`.
- Implementation: not this skill. Hand off to `spec-driven` Execute, `spec-driven-lean` Build, or the source's `tlc-implement`.
- `specs` remains the AEOS mutating preflight when later implementation will change the repo.

## Activation

- User says `tlc-plan`, write the task, cut this PRD into tasks, or turn this design doc into work.
- A decided source exists (PRD, TDD, RFC, one-line ticket, thread).

## Non-activation

- No decision yet (blank wish).
- User asked only to implement an existing task.
- User asked for `spec-driven` or `spec-driven-lean` on the same feature unless they switch workflows.

## Critical rules

1. Every criterion is an observable outcome with a concrete value. Refuse rather than guess.
2. Default to one task per source. Split only for an order constraint, an external blocker, or another team. Show seams; do not invent a task count.
3. When the source contradicts the code, amend the source.
4. Surface walk and nine-dimension sweep record landings (`existing`, `n/a`, `Unresolved`) — they do not invent criteria.
5. Read `references/document-format.md` only when writing `.tasks/<name>.md`, after Cut, Ground, Walk and Sweep.
6. Follow `references/ORIGINAL_SKILL.md` for cut/ground/walk/sweep, question limits and output shape.
7. Knowledge chain: code and conventions, project docs, official library docs, web, then flag as uncertain.

## Continuity

`.tasks/` is the task record for this skill. Material AEOS missions still use the continuity quartet. Do not persist secrets.
