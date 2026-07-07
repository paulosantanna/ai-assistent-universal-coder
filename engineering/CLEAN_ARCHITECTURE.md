# CLEAN_ARCHITECTURE.md

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

Define clean architecture usage.

## Dependency direction

Dependencies point inward.

Domain must not depend on infrastructure.

## Layers

- Domain
- Application
- Interface adapters
- Infrastructure
- Delivery mechanisms

## Rules

- Business rules live in domain/application.
- External systems are adapters.
- Frameworks are details.
- Tests should target business behavior independently of infrastructure.
- Do not leak ORM models into domain unless consciously accepted.

## Violations

- controllers containing business rules;
- database code inside domain;
- direct cloud SDK calls in use cases;
- circular dependencies;
- infrastructure driving domain design.
