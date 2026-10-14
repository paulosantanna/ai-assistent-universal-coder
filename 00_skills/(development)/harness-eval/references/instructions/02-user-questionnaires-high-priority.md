<!-- Package: 00_skills/(development)/harness-eval; relative command/resource examples resolve from that package or workspace root. -->

## User questionnaires (HIGH PRIORITY)

**Stop and ask before continuing.** Do not skip these gates. Do not silently include optional docs or spawn B/C judges.

Order after inventory: **Q1 (if needed) → Q2 → then Track A** (A always runs) → B/C only if approved.

### Q1 — Optional project docs (after inventory)

When `optional-docs-candidates.md` lists optional types, ask before Q2 / Track A:

```markdown
Inventory found cited project docs outside the agent skill trees.

- **Always in scope:** skill-tree files (`.agents/skills`, `.cursor/skills`, `.claude/skills`)
- **Always excluded:** ADRs / RFCs / decision-record trees (never scored as T2)
- **Optional (default: omit):** see types/paths in `optional-docs-candidates.md`

Include any optional doc types or paths in this run?
Reply with: `none` (default), type ids (e.g. `docs`), and/or specific paths.
```

Re-run inventory with `--include-doc-type` / `--include-doc` only after the user answers. If no optional types, skip Q1.

### Q2 — Tracks B and C (before Track A — budget)

Ask **before** Track A so the user sets spend up front. Track **A always runs** next (deterministic, ~0 model tokens). B/C run only if approved.

```markdown
Choose eval scope for this run (before Track A).

| Track | Question | Certainty | Token consumption |
|-------|----------|-----------|-------------------|
| **A — Correctness** | Cited path/command exists? | **Highest** — script only, no LLM. Prefers false negatives over false BROKEN. | **~0 model tokens** (always runs next) |
| **B — Redundancy** | Would an agent rediscover this cheaply without the harness? | **Medium** — dual LLM + plants; Ship only if trap PASS and both agree. Disagree → Hold. Less model-sensitive than C. | **High** — 2 judges × every claim (~N in this inventory). Each may spot-check the repo. |
| **C — Usefulness** | Does this surface change behavior vs theory/demo/overlap? | **Lowest / most subjective** — dual LLM + plants + fan-in; **model-sensitive**. Slim/Mixed need gates; prefer second-model check before large deletes. | **Highest** — 2 judges × every surface (whole files; often dominates the run). |

Notes: Ship (B) ≠ Slim (C). Rediscoverable ≠ useless. A always runs; B/C are optional.

Reply with one of: `A only`, `B`, `C`, or `B+C`.
```

Fill claim count from `claims.md` when known; surface count ≈ T0+T1+T2 markdown after extract (or say “after surfaces_extract” if not run yet).

- **`A only`:** run Track A; present `04`; stop (no B/C judges).
- **`B`:** Track A, then Steps 4–6.
- **`C`:** Track A, then Steps 7–10 (C does not need B).
- **`B+C`:** Track A, then Steps 4–11.

If the user already requested B/C/`full eval` in the triggering message, treat as approval — still show the Q2 table once so costs are visible.
