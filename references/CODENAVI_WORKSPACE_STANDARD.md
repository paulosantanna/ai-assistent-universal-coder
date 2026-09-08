# CodENavi Workspace Standard

Version: 1.0.0
Status: mandatory
Applies to: all AEOS agents, subagents, skills, playbooks, MCPs, LCPs, tools and human-authored changes.

## Mission lifecycle

Every material task follows six explicit phases:

1. BRIEFING — intent, acceptance criteria, assumptions, risks, constraints, relevant skills.
2. RECON — current code, tests, config, architecture, `.notebook/`, dependencies and authoritative docs.
3. PLAN — minimal ordered steps with verification checkpoints and rollback when relevant.
4. EXECUTE — surgical implementation only within scope.
5. VERIFY — repository-native deterministic checks and evidence.
6. DEBRIEF — evidence, notebook/memory updates, residual risks, handoff.

## Coding principles

- Think before coding; state uncertainty instead of guessing.
- Simplicity first: minimum code that solves the stated problem.
- Surgical changes: do not improve adjacent code unless the mission requires it.
- Respect the codebase: naming, organization, imports, style, error conventions and architectural boundaries.
- Prefer official, current language/framework best practices when local conventions do not define behavior.
- Before adding a dependency, verify that the project does not already contain an equivalent capability.
- Handle realistic failures; never add theatrical catch blocks for impossible states.
- Tests prove behavior/contracts, not internal implementation.
- Bug fix: reproduce → fix root cause → retain regression coverage where technically possible.
- Comments explain non-obvious WHY. Never remove existing comments unless proven wrong.

## Knowledge verification

Never rely solely on model training memory for API signatures, framework behavior or dependency semantics.

Verification chain:
`.notebook/ → repository code/docs → governed MCP/LSP/context → official docs → web → explicit uncertainty`

## Notebook intelligence

- Read `.notebook/INDEX.md` before every material mission when present.
- INDEX: one line per note, short summary, category and 2–4 discriminative tags.
- Notes are telegraphic field notes, not duplicated documentation.
- Prefer pointers such as `path/file.ts:function()` or `path/file.ts (L10-25)` instead of pasted source.
- One concept per note. Split when scrolling becomes necessary.
- Include entry point and `Updated:` date.
- Categories: `flows`, `patterns`, `gotchas`, `domain`, `graph`.
- Start flat. After roughly 15 active notes, organize into category folders.
- Archive inactive/stale notes instead of loading them by default.
- If implementation invalidates a note, update/deprecate it before mission completion.

## Goal-driven execution

Turn vague requests into observable acceptance criteria. Examples:

- “add validation” → define accepted/rejected inputs and tests.
- “fix bug” → reproduce the defect, identify root cause, verify no regression.
- “refactor X” → establish before/after behavior equivalence and measurable motivation.

## Secret handling

Credentials, tokens, cookies, private keys and passwords:

- live only in approved runtime/secret providers;
- are never printed, echoed, committed, copied into chat/prompts, evidence or memory;
- are masked during inspection;
- use least privilege and short-lived credentials where possible;
- a credential exposed by accident is treated as compromised and must be rotated.

Authenticated actions are read-only by default unless a governed mutation path explicitly grants write scope.

## Documentation and notes

No stale documentation. If behavior changes, update the smallest authoritative document/note that describes it. Avoid duplicating the same rule across files: use pointers and canonical ownership.

## Completion rule

A task is not complete until scoped behavior is verified, evidence exists, stale knowledge caused by the change is repaired, and blocking risks are either resolved or explicitly approved through AEOS governance.
