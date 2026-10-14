<!-- Package: 00_skills/(development)/spec-driven-eval; relative command/resource examples resolve from that package or workspace root. -->

## Calibration (do this once per PRD, before trusting a benchmark)

The checklist is a hypothesis about what each AC means; calibrate it so different evaluators agree:

1. **Anchor.** `references/reference.md` holds worked checklist anchors — at least one clearly-MET, one clearly-UNMET, and one borderline check with the verdict and reasoning. Read them before scoring; they fix where the MET/UNMET boundary sits.
2. **Agreement check.** For a high-stakes benchmark, have the checklist reviewed against a human-labeled reference (or a second judge model). If verdicts disagree on more than ~20% of checks, the **checklist wording is too vague** — sharpen the ambiguous checks in `_ac-baseline.md` and re-run. Do not "average away" disagreement; fix the operational definition.
3. **Borderline cases are the valuable ones.** When you find a check humans/judges split on, add it to the anchor pool in `references/reference.md` with the resolved verdict.

---
