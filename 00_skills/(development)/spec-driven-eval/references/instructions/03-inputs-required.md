<!-- Package: 00_skills/(development)/spec-driven-eval; relative command/resource examples resolve from that package or workspace root. -->

## Inputs required

1. **The PRD** (ground-truth product intent) — the user story acceptance criteria are the unit of evaluation.
2. **The implementation** (production code).
3. **The tests** (unit + e2e).
4. **The SDD-derived artifacts** — `spec.md` and `tasks.md` (refined ACs, requirement IDs, derived requirements). Required for the Elicitation `E` and Scope `S` axes (they grade *these* against the PRD). When absent, `Final`/`T` still run, but report `E`/`S` as `n/a — no derived spec`. The **PRD remains the source of truth** for what counts as "expected"; the derived spec is what gets graded for respect and extraction.

**Scoping the diff.** Before scoring, use git to identify which files changed for this implementation. That **diff surface** is the primary search scope for all `file:line` evidence in steps 4 and 8:

```bash
git diff <base>..<head> --name-only   # branch or PR
git diff --name-only HEAD             # uncommitted changes
git status --short                    # include untracked new files
```

Record the diff surface in the report. Evidence outside it is still valid (e.g. a pre-existing file was modified), but note when a check relies on files not in the diff — that may indicate the wrong base was chosen.

---
