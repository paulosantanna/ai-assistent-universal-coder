# ARCHITECTURE_REASONING.md

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

Guide architecture decisions with Staff/Chief-level discipline.

## Architecture analysis dimensions

- domain boundaries;
- data flow;
- dependency direction;
- coupling/cohesion;
- scalability;
- reliability;
- failure modes;
- security boundaries;
- observability;
- deployment topology;
- testability;
- migration path;
- operational cost.

## Architecture decision process

1. Define problem.
2. Identify constraints.
3. Describe current architecture.
4. Generate alternatives.
5. Analyze trade-offs.
6. Select decision.
7. Write ADR.
8. Define validation.
9. Define review trigger.

## Decision quality

A decision is weak if:
- alternatives are missing;
- trade-offs are hidden;
- migration path is unclear;
- rollback is impossible;
- tests are not defined;
- operational impact is ignored.

## Architecture principle

Architecture should make correct behavior easy and incorrect behavior difficult.
