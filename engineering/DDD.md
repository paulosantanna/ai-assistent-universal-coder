# DDD.md

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

Use Domain-Driven Design when domain complexity justifies it.

## Concepts

- bounded context;
- aggregate;
- entity;
- value object;
- domain service;
- application service;
- repository interface;
- domain event;
- ubiquitous language.

## Rules

- Use DDD to model business complexity, not as ceremony.
- Do not create aggregates for simple CRUD unless complexity exists.
- Keep invariants close to the aggregate.
- Use value objects for meaningful domain concepts.
- Respect bounded context boundaries.

## Output

DDD work should produce:
- context map;
- aggregate map;
- invariants;
- domain events;
- application services;
- persistence boundaries.
