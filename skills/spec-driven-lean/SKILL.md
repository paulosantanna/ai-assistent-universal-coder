---
name: spec-driven-lean
description: "Assimilated Tech Lead's Club lean spec workflow (tlc-spec-lean 1.0.0). Freeze obligations in plan + proof-backed checks, then build, then independent verify. Triggers: spec-driven-lean, tlc-spec-lean, plan feature, write the checks, build this plan, verify work. Do not use when a formal task list already exists or for standalone design docs."
---

# Spec-Driven Lean

Assimilated from installed `tlc-spec-lean` 1.0.0 (Tech Lead's Club). Derived from `tlc-spec-driven` 3.3.0. Original contract: `references/ORIGINAL_SKILL.md`.

## Identity

A skill of the single canonical `codenavi-agent`. It creates no new agent identity. Source "sub-agent" roles are internal lenses / sequential work units.

## Mission

Freeze obligations, not the plan. Four moves: Plan → Checks → Build → Verify. One human-reviewed `plan.md`, then proof-backed `checks.md`, then implementation, then an independent verifier. No task catalogue and no component catalogue.

## Relationship to AEOS `specs` and `spec-driven`

`specs` remains the AEOS mutating-skill preflight. Use this skill when the user wants lean obligation-first feature work. Do not run `spec-driven` (full specify/design/tasks) on the same feature unless the user switches workflow. A current approved `plan.md` + `checks.md` may satisfy `specs` evidence when checks carry observable claims, proofs and approval. It does not waive security, continuity or human-approval gates.

## Activation

- User asks for `spec-driven-lean`, `tlc-spec-lean`, plan feature, write the checks, build this plan, verify work.

## Non-activation

- Standalone design documents unattached to a feature.
- Architecture decomposition analysis.
- Work that already has a task list or checklist to execute (`spec-driven` or another executor).
- Read-only inspection that produces no `.specs/` artifact.

## Critical rules

1. Resolve `<skill-dir>` as the directory that contains this `SKILL.md`. Run `python`/`py -3`/`python3` as `<skill-dir>/scripts/<name>.py`. Project data stays under `.specs/`; pass `--root` when cwd differs.
2. Every check is one observable claim with a concrete value plus the proof whose exit code settles it. No proof, no check.
3. Tests assert what the checks say, never what the code happens to do.
4. Never weaken, delete or skip a test to pass. A wrong check is stop-and-ask.
5. Checks and `Test policy` rows are fixed once approved. `Landing`, `Relations` and `Surface` are additive. `Flow` and `Impact` stay true.
6. `VerifierLens` is dispatched by the orchestrating turn, never by the builder, over `<feature base>..HEAD` with every check. The builder does not write `verification.md`.
7. Completion requires `<skill-dir>/scripts/validate_verification.py` exit 0.
8. Approved plan/checks authorize local edits and local commits only when the user has authorized commits. `git push`, deploy and production data changes need an explicit go-ahead.

## Profile

Default when undeclared: `light`. Declare the floor in skill policy or the user request, not by inventing a second agent constitution.

| Profile | Adds | Cannot catch |
| --- | --- | --- |
| `light` (default) | proofs at HEAD, one located assertion per check, swept existing | set member with no proof; test that passes under a wrong implementation |
| `standard` | recomputed Coverage join, Test policy verdicts, one fault per assertion surface | check that contradicts a binding source; a screen nobody built |
| `ui` | binding sources compared, per-screen copy and arrangement | only spacing, colour and type weight |

Where the profile looks too thin, say so in one line and let the user raise it.

## Artifacts

```
.specs/
├── STATE.md
├── LESSONS.md
├── lessons.json
└── features/<feature>/
    ├── plan.md
    ├── checks.md
    └── verification.md
```

For a change under roughly three files with no one-way door, write only `checks.md` with `## Intent` and skip `plan.md`.

## Continuity

`.specs/STATE.md` is feature-session memory for this skill. Material AEOS missions still use the continuity quartet. Promote only verified durable facts into `MEMORY.md`. Do not copy secrets into `.specs/` or the notebook.

## Lenses (never new agents)

- `PlanLens` — `references/plan.md`
- `ChecksLens` — `references/checks.md`
- `BuildLens` — `references/build.md`
- `VerifierLens` — `references/verify.md`
- `MemoryLens` — `references/memory.md`

Source batch/handoff text is remapped to sequential work units of `codenavi-agent`. Do not spawn additional agent identities.

## Scripts

| When | Command |
| --- | --- |
| Before presenting the plan | `validate_plan.py <feature>` |
| Before starting to build | `validate_checks.py <feature>` |
| Before each authorized commit | `check_commit.py --message "<msg>"` |
| Before declaring done | `validate_verification.py <feature>` |
| After editing a validator or template | `selftest.py` |

Non-zero exit means STOP and fix. Degrade to manual artifact reading only when Python cannot run.

## Knowledge verification chain

Existing code → project docs → official library docs → web search → flag as uncertain. Never invent an API, flag, command or behaviour.

## Output behavior

Produce the artifact; do not narrate the phase. Lead with the verdict. Section headings stay in English; identifiers are never translated.
