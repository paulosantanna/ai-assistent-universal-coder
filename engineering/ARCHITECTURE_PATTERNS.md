# ARCHITECTURE_PATTERNS.md

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

Guide selection of architecture patterns.

## Patterns

- modular monolith;
- layered architecture;
- clean architecture;
- hexagonal architecture;
- microservices;
- event-driven architecture;
- CQRS;
- DDD;
- pipeline architecture;
- plugin architecture;
- data lakehouse;
- RAG architecture;
- ML platform architecture.

## Selection criteria

Select based on:
- domain complexity;
- team size;
- operational maturity;
- deployment constraints;
- scaling needs;
- data consistency;
- compliance;
- testability.

## Rule

Do not choose microservices because they sound advanced.
Choose them only when independently deployable bounded contexts justify operational complexity.
