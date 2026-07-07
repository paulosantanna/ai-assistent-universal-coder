# PLANNING_ENGINE.md

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

Convert objectives into executable, verifiable engineering plans.

## Planning inputs

- user objective;
- repository context;
- architecture constraints;
- risk model;
- available tools;
- previous knowledge;
- acceptance criteria.

## Planning output

A plan must include:

```json
{
  "objective": "string",
  "scope": "string",
  "out_of_scope": [],
  "acceptance_criteria": [],
  "risks": [],
  "specialists": [],
  "task_graph": [],
  "verification_plan": [],
  "rollback_plan": [],
  "knowledge_outputs": []
}
```

## Planning algorithm

1. Restate the objective.
2. Classify domain and risk.
3. Identify affected architecture areas.
4. Identify missing context.
5. Inspect required evidence.
6. Break into phases.
7. Identify specialists.
8. Define task dependencies.
9. Define validation gates.
10. Define stop conditions.

## Plan quality criteria

A good plan is:
- scoped;
- testable;
- delegated;
- risk-aware;
- reversible;
- evidence-driven;
- adaptable.

## Anti-patterns

Reject plans that:
- start coding before understanding;
- require massive rewrites without evidence;
- ignore tests;
- ignore security;
- omit rollback;
- have vague completion criteria;
- assign all work to ROOT.
