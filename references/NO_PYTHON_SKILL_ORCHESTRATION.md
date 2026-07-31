# AEOS No-Python Skill Orchestration

## Intent

AEOS must evolve into a skill-orchestrated WorkspaceSO where user requests are
routed to the best available skills automatically. The user must not need to
name the skill unless they want to override routing.

## Immutable Rules

1. New AEOS runtime orchestration must be implemented in Node/TypeScript or
   declarative skill/playbook contracts.
2. Python is removed from the WorkspaceSO runtime path.
3. Python source and project metadata are not allowed in the AEOS workspace.
4. Every routed request must write Chromatic Mega Brain memory artifacts:
   `MEMORY.md`, `LEARNING.md`, `HANDOFF.md`, and `PROGRESS.md`.
5. A request may not be considered complete when routing, handoff, progress, or
   memory persistence failed.
6. Skill selection is automatic by default and explicit by override.
7. Architecture-changing work requires explicit user intent.
8. Skill creation must use the project skill builder/factory contract.

## Runtime Model

```mermaid
flowchart TD
    U[User Request] --> R[Skill Router]
    R --> C[Capability Match]
    C --> S[Selected Skills]
    S --> H[Handoff Record]
    H --> P[Progress Record]
    P --> M[Chromatic Memory]
    M --> E[Execution or Plan]
    E --> J[Judge / Verification]
```

## Skill Routing Contract

The router must inspect:

- skill id;
- mission;
- capabilities;
- owner agent;
- risk level;
- skill path;
- request keywords;
- explicit user constraints.

The router output must include:

- selected skills;
- rejected skills when relevant;
- assumptions;
- routing evidence;
- memory write result;
- handoff target;
- progress status.

## Python Removal Contract

Python is removed as an implementation language for AEOS orchestration. The
workspace must not contain:

- `*.py`;
- `*.pyc`;
- `pyproject.toml`;
- `pytest.ini`;
- `behave.ini`;
- `requirements*.txt`.

Historical recovery is handled through Git history and review bundles, not by
keeping Python files in the active workspace.

## Production Gate

Before declaring no-Python readiness:

1. `node scripts/aeos-skill-router.mjs "health check"` succeeds.
2. `node scripts/aeos-no-python-guard.mjs` reports zero Python blockers.
3. `npm --prefix runtime run build` succeeds.
4. All active Node tests pass.
5. Chromatic memory files are updated for the execution.
