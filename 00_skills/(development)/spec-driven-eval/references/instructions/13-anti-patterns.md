<!-- Package: 00_skills/(development)/spec-driven-eval; relative command/resource examples resolve from that package or workspace root. -->

## Anti-patterns

- Scoring `I`/`T` on a sliding "feels like a 0.75" judgment instead of counting binary checks.
- Re-deriving the AC list or checklist per implementation (breaks comparability) instead of reusing the frozen baseline.
- Marking a check UNMET without showing the search performed; or MET without `file:line` evidence.
- Searching the full codebase for evidence without first running `git diff` to bound the diff surface — this produces unreliable searches and inflates "not found" confidence.
- Awarding implementation credit without reading the production code path end-to-end.
- Counting extra/defensive tests toward an AC's required coverage, or letting more code/tests raise the grade.
- Reporting an Engineering Gate as passing without running it; or applying `Adjusted Final` for a `not-run` gate.
- Marking a gate `not-run` without a recorded attempt (command + error output). "Infra not available" without a probe is fabricated evidence.
- Fixing the code under evaluation to turn a red gate green — the evaluator is read-only over the subject; a red gate is scored `✗` and the fix goes in the report.
- Hand-computing the roll-up (`Σw`, `Final`) instead of executing it as a script and pasting the output.
- Penalizing missing out-of-scope features.
- Folding `E` or `S` into `Final` — the headline grade must mean only "fidelity to the given PRD" or comparability breaks.
- Penalizing a valid requirement the framework extracted but correctly *deferred* as out-of-scope (that is good discipline, not a scope failure).
- Scoring harness completeness (`T`) against the PRD alone — the denominator is the sanctioned set (PRD ACs ∪ valid E-additions).
- Rewarding requirement *volume* in `E`: hallucinated/scope-creep additions lower `E_precision`, they don't raise the score.
- Changing the weights (`0.6/0.4`, P0/P1/P2) between implementations of the same PRD.
