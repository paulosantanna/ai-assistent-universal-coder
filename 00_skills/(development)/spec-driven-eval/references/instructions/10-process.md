<!-- Package: 00_skills/(development)/spec-driven-eval; relative command/resource examples resolve from that package or workspace root. -->

## Process

Copy this checklist and track progress:

```
FRAMEWORK — respect & extract requirements
- [ ] 1. Locate PRD, spec.md/tasks.md. Run git diff to identify changed files (diff surface). Use the diff surface as the primary search scope for implementation and test evidence throughout steps 4 and 8
- [ ] 2. Enumerate stories + ACs; tag priority; mark out-of-scope items
- [ ] 3. Build/load the frozen binary checklist per AC (I-checks + T-checks) → _ac-baseline.md
- [ ] 4. Score I-checks MET/UNMET with file:line evidence (record searches before any UNMET)
- [ ] 5. Elicitation E: run the category rubric (E_recall) + added-requirement ledger (E_precision, E_justified) → freeze the `valid E-additions` set
- [ ] 6. Scope S: trace every built behavior (PRD-boundary / rogue-build / plan-drift)

HARNESS — ensure they are all implemented
- [ ] 7. Define the sanctioned set = PRD ACs ∪ valid E-additions; ensure each has a T-check
- [ ] 8. Score T-checks MET/UNMET with file:line evidence (unit + e2e per fixed level policy)
- [ ] 9. Inventory extra tests → Robustness Index R
- [ ] 10. Classify every feature test into tiers → Test Distribution D (counts + %)
- [ ] 11. Run/record Engineering Gates G (✓/✗/not-run)

ROLL-UP
- [ ] 12. Repeat the scoring steps three times (k=3); take majority verdict per check
- [ ] 13. Compute I, T, AC/Story/Final; apply bands; Adjusted Final only if a gate is ✗
- [ ] 14. Emit the report (see references/reference.md template): Final + E + S + R/G/D + ranked gaps + fixes
```

**Step rules:**

- **Step 1** — Identify the diff surface before any evidence search. Pick the base that matches what you are evaluating (branch tip, last commit, or working tree):

```bash
git diff <base>..<head> --name-only   # for a branch/PR
git diff --name-only HEAD~1           # for the last commit
git diff --name-only HEAD             # for uncommitted changes
git status --short                    # for untracked new files
```

Record the file list in the report. Steps 4 and 8 use it as the first set of paths to inspect.
- **Step 2** — Out-of-scope items from the PRD's explicit out-of-scope / non-goals section (whatever heading the PRD uses) get `w=0`. Absence is **not** a defect. Do not score them.
- **Step 3** — Reuse the existing `_ac-baseline.md` if present; otherwise create it and treat it as the contract for all future runs of this PRD. Include only observable-behavior clauses as checks.
- **Step 5** — `E` grades `spec.md`/`tasks.md`, not code. The ledger's *valid* additions define the `valid E-additions` set used by Steps 6 and 7. Mark each valid addition built/deferred.
- **Step 6** — Traceability: a built behavior with no PRD AC and no valid `E`-addition is a rogue build (`fail`). A deferred-valid out-of-scope addition is **not** a penalty.
- **Step 7** — The harness denominator is the **sanctioned set (PRD ACs ∪ valid E-additions)**. A valid extracted requirement with no test is a `T` miss, not an `E` miss.
- **Step 8** — Binary only: MET (evidence) or UNMET (searched, absent). No partial per-check values.
- **Step 9** — Extra tests are a positive signal but never substitute for missing coverage. A high `R` with low `T` is still a low grade.
- **Step 10** — Each test lands in exactly one tier; counts must sum to the total feature-test count. Exclude pre-existing tests not added by the feature (note them separately).
- **Step 11** — A gate is `✓`/`✗` only if actually executed; otherwise `not-run` with the **attempt evidence** (command + error output — see Probe-before-not-run). Do not assume infra is unavailable: check it (e.g. `docker ps`, or whatever the project's own docs say the e2e suite needs running). If a gate is red, do NOT fix the subject code (Core rule 5).
- **Step 12** — Majority over k=3. Note any check where the three passes disagreed.
- **Step 13** — Show the arithmetic: list MET/total per check set so `I` and `T` are recomputable. Execute the roll-up as a script and paste its output (Reproducibility rule 4) — never hand-compute `Σw` or `Final`.

---
