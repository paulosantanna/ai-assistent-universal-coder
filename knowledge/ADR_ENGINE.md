# ADR_ENGINE.md

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

Persist architecture decisions as first-class knowledge.

## ADR template

```markdown
# ADR-000X: Title

## Status
Proposed | Accepted | Rejected | Superseded | Deprecated

## Context

## Problem

## Constraints

## Options considered

## Decision

## Rationale

## Consequences

## Risks

## Validation plan

## Review trigger

## Evidence
```

## When to create ADR

Create ADR when:
- architecture boundary changes;
- technology is selected;
- database changes;
- cloud/deployment model changes;
- security model changes;
- AI/RAG/ML pipeline changes;
- clinical governance changes;
- public API changes;
- irreversible migration occurs.

## Rule

Major architecture without ADR is undocumented architecture debt.
