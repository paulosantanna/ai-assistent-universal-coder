<!-- Package: 00_skills/(development)/spec-driven-eval; relative command/resource examples resolve from that package or workspace root. -->

## Core rules (read first)

These five rules govern every score. They exist to make the grade auditable and reproducible.

1. **Evidence or zero.** Every MET check MUST cite evidence as `file:line` (or `file:startLine-endLine`). No located evidence ⇒ the check is UNMET. Never award credit from assumptions or from the PRD restating intent.
2. **Search-before-zero (anti false-negative).** Before marking a check UNMET for "not found", record the search actually performed — starting with the diff-surface files from the scoping step, then the grep/glob terms tried and any additional files/dirs inspected. A check scored UNMET must confirm the behavior is absent from the diff surface, not just from an ad-hoc grep across the full repo. UNMET means *searched and genuinely absent*, not *did not look*. If no search is shown, the check is **not yet scored**, not UNMET.
3. **Read the path end-to-end — including the data shape.** A check is MET only if you traced the real code/test path, not because a symbol name matches. For an emitted/returned/persisted artifact, **inspect the constructed payload object itself**, not just the call site — a present `emit(...)`/`return ...` does not prove the named field is in the payload (see the Conjunction rule). A test that *exercises* a behavior but does not *assert* it does **not** meet a verification check.
4. **Judge ≠ author for benchmarks.** When grading to compare implementations, the evaluating model should differ from the model that wrote the code; LLM judges over-reward their own output (self-preference bias). If they are the same, flag it under *Assumptions* and treat borderline checks as UNMET.
5. **The evaluator is read-only over the subject.** Never modify the code under evaluation — not to fix a failing gate, not to "help", not even for trivial type errors. A red gate stays red: record `✗`, apply the `Adjusted Final`, and put the required correction in the report's fix list. Modifying the subject mid-evaluation contaminates the benchmark (the grade no longer measures the framework's output) and invalidates the diff surface. If a correction was accidentally applied, revert it and score the original state.

---
