# LANGUAGE_STANDARDS.md

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

Apply mature standards per language.

## Java

Use:
- supported JDK version;
- Maven/Gradle conventions;
- JUnit;
- Mockito/Testcontainers where appropriate;
- SpotBugs/Checkstyle/PMD if configured;
- Spring conventions when Spring exists;
- dependency management discipline.

## Python

Use:
- type hints;
- pytest;
- ruff/black/mypy when applicable;
- async only where justified;
- dependency isolation;
- explicit exceptions.

## TypeScript/Node

Use:
- strict TypeScript;
- eslint/prettier;
- npm/pnpm/yarn conventions;
- Jest/Vitest/Playwright where applicable;
- runtime validation for external inputs.

## Universal rule

Respect existing project conventions unless evidence shows they are harmful.
