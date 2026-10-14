<!-- Package: 00_skills/(development)/spec-driven-eval; relative command/resource examples resolve from that package or workspace root. -->

# Spec-Driven Implementation Evaluation

Evaluate a spec-driven-development (SDD) effort against a PRD **case by case** (acceptance criterion by acceptance criterion), scoring **implementation** and **tests** separately, and roll up to a single comparable final grade. Designed for benchmarking: the same PRD evaluated across different SDD frameworks — and the same effort evaluated twice — must yield comparable, reproducible numbers.

### Two subjects, two questions

This eval answers two independent questions, and keeps their verdicts separate because they fail independently:

1. **How good is the framework at respecting and extracting requirements?** — Did it honor the PRD and stay in bounds (*respect*: `Final` implementation side + Scope `S`), and did it surface the implicit requirements the PRD only implied, without noise (*extract*: Elicitation `E`)?
2. **How good is the harness at ensuring they are all implemented?** — Does the test suite prove every sanctioned requirement is actually built (`T` + Engineering Gates `G`)?

> **The linkage that makes "all implemented" well-defined:** the harness is held accountable for the **full sanctioned requirement set = `PRD acceptance criteria ∪ valid E-additions`**. A valid requirement the framework extracted but the harness never tests is a *harness* miss (`T`), not a framework miss (`E` keeps the extraction credit). Extraction defines the verification target.

Scoring is **checklist-based**: every criterion is decomposed into atomic binary (MET / UNMET) checks, each backed by `file:line` evidence. Binary decomposition is the design choice that makes the grade reproducible — graded/Likert scales (`is this a 3 or a 4?`) are the dominant source of evaluator-to-evaluator disagreement; binary checks raise inter-evaluator agreement to roughly human level. Partial credit is **derived** from the fraction of checks met, never judged on a sliding scale.
