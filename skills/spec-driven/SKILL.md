---
name: spec-driven
description: "Assimilated Tech Lead's Club spec-driven workflow (tlc-spec-driven 3.3.0). Use for specify/design/tasks/execute feature work, EARS requirements, atomic tasks, validation scripts and independent verification. Triggers: spec-driven, tlc-spec-driven, specify feature, design, tasks, implement, validate, verify work. Do not use for standalone architecture documents unattached to a feature."
---

# Spec-Driven

Assimilated from installed `tlc-spec-driven` 3.3.0 (Felipe Rodrigues / Tech Lead's Club). Original contract: `references/ORIGINAL_SKILL.md`.

## Identity

A skill of the single canonical `codenavi-agent`. It creates no new agent identity. Source "sub-agent" roles are internal lenses / sequential work units.

## Mission

Plan and implement features with auto-sized depth: Specify → (Design) → (Tasks) → Execute. Produce testable EARS requirements, optional design and atomic tasks, then implement against those artifacts with scripted structural gates and an independent verifier pass.

## Relationship to AEOS `specs`

`specs` remains the AEOS mutating-skill preflight. This skill is the feature workflow. A current `.specs/features/<feature>/spec.md` (plus tasks/validation when those phases ran) may satisfy `specs` evidence when it carries testable requirements, acceptance criteria, evidence gates and approval. It does not waive security, continuity or human-approval gates.

## Activation

- User asks for `spec-driven`, `tlc-spec-driven`, specify/design/tasks/implement/validate a feature.
- Feature planning with traceable requirements and verified implementation.

## Non-activation

- Pure architecture decomposition with no feature to implement.
- Standalone design documents unattached to a feature.
- User explicitly chose `spec-driven-lean` for the same feature.
- Read-only inspection that produces no `.specs/` artifact.

## Critical rules

1. Resolve `<skill-dir>` as the directory that contains this `SKILL.md`. Read referenced files completely. Run `python`/`py -3`/`python3` as `<skill-dir>/scripts/<name>.py`. Project data stays under `.specs/` at the project root; pass `--root` when cwd differs.
2. Tests assert spec-defined outcomes, never the implementation.
3. A task is done only when its gate passes.
4. One atomic local commit per formal task **only when the user has authorized commits**. Otherwise mark task state and stop for explicit commit approval. Never weaken or delete tests to pass.
5. After the last task, the `VerifierLens` always runs. Author of the implementation must not write `validation.md`.
6. Approved spec/tasks authorize local implementation only. `git push`, force-push, deploy, production DB changes and other remote/destructive operations need an explicit go-ahead for that action.
7. Non-zero validator exit means STOP and fix.

## Deterministic gates

- Before confirming a spec: `<skill-dir>/scripts/validate_spec.py <spec-path-or-feature>`
- Before presenting tasks: `<skill-dir>/scripts/validate_tasks.py <tasks-path-or-feature>`
- On each authorized commit: `<skill-dir>/scripts/check_commit.py --message "<msg>"`
- Before declaring done: `<skill-dir>/scripts/validate_state.py <feature>`
- Confirmed lessons: `<skill-dir>/scripts/lessons.py list --status confirmed`

Skip a script only when no code-execution tool exists; then perform the same checks by reading the artifact and say once that the path is degraded.

## Auto-sizing

| Scope | Specify | Design | Tasks | Execute |
| --- | --- | --- | --- | --- |
| Small (≤3 files, one sentence) | Inline one-liner | Skip | Skip | Implement + verify inline |
| Medium (clear feature, <10 tasks) | Brief spec | Inline | Implicit | Implement + verify |
| Large | Full spec + IDs | Architecture | Full breakdown | Per-task verify |
| Complex | Full spec + discuss | Research + architecture | Breakdown + phases | Implement + UAT |

Specify and Execute are always required. If Tasks was skipped and Execute lists >5 steps or complex dependencies, stop and write `tasks.md`.

## Artifacts

```
.specs/
├── STATE.md
├── LESSONS.md
├── lessons.json
└── features/<feature>/
    ├── spec.md
    ├── context.md      # only when discuss runs
    ├── design.md       # Large/Complex
    ├── tasks.md        # Large/Complex
    └── validation.md   # VerifierLens only
```

Create files lazily. Absence means the phase was skipped.

## Continuity

`.specs/STATE.md` is feature-session memory for this skill. Material AEOS missions still use `.notebook/HANDOFF.md`, `MEMORY.md`, `PROGRESS.md` and `LEARNING.md`. Promote only verified durable facts into `MEMORY.md`. Do not copy secrets into `.specs/` or the notebook.

## Lenses (never new agents)

- `SpecifyLens` — `references/specify.md`, `references/discuss.md`
- `DesignLens` — `references/design.md`
- `TasksLens` — `references/tasks.md`
- `ExecuteLens` — `references/implement.md`
- `VerifierLens` — `references/validate.md`; independent pass; author ≠ verifier
- `MemoryLens` — `references/memory.md`, `references/lessons.md`

Source batch/worker text in `references/sub-agents.md` is remapped: sequential work units of `codenavi-agent`, never spawned agent identities. Offer-then-confirm still applies before splitting large task batches.

## Knowledge verification chain

1. Codebase conventions
2. Project docs and `.specs/STATE.md`
3. `.notebook/` then governed MCP/LSP/docs
4. Official documentation / web
5. Flag as uncertain — never invent APIs or behavior

## Output behavior

Produce the artifact; do not narrate the phase. Lead with the verdict. Writing rules: `references/coding-principles.md`.
