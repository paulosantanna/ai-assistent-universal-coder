<!-- Package: 00_skills/(development)/spec-driven-eval; relative command/resource examples resolve from that package or workspace root. -->

## Reproducibility rules

The grade must be stable: the **same PRD + same commit** must yield the **same `Final`** across runs and evaluators. Obey all of:

1. **Freeze the AC list AND its checklist (the single biggest drift source).** AC enumeration and check granularity are decided **once** and pinned, because both `I`, `T`, and the `Story_score` denominator depend on them:
   - If `spec.md` with stable requirement IDs exists, the AC list and IDs are frozen — use them verbatim; do not re-split or merge.
   - Derive the binary checklist for each AC once and persist it to `<spec-folder>/evaluations/_ac-baseline.md` (IDs + verbatim AC text + the I-checks and T-checks). **Every implementation of that PRD is scored against the identical checklist.**
   - One AC = one testable assertion of intent; one check = one atomic, observable yes/no proposition. Do not collapse distinct behaviors into one check, nor split one behavior across several.
2. **Priority comes from the PRD, never inferred silently.** Use the PRD's explicit P0/P1/P2 labels. If a story is unlabeled, mark its priority `ASSUMED` in the report and list it under *Assumptions*; never let an inferred priority silently move the `3/2/0` weights.
3. **Round once, at the end.** Carry full precision through the arithmetic; round only the reported `AC_score`, `Story_score`, and `Final` to **2 decimals**. Band assignment uses the rounded `Final`.
4. **Compute, don't calculate.** The roll-up (`Σw`, every `Story_score`, `Final`, `Adjusted Final`) MUST be computed by executing a script (e.g. `node -e` / `python3 -c`) that takes the per-AC `I`/`T` fractions and the priority-weight table as input, with the script's output pasted into the report. Never do the arithmetic mentally or by hand — a hand-summed denominator (`Σw`) is a known failure mode that silently shifts the grade band. `Σw` must be derived inside the script from the same priority table shown in the report, not typed in as a literal.
5. **Self-consistency ensemble (k = 3).** Evaluate the checklist **three times independently** at low/zero temperature and take the **majority MET/UNMET per check** before computing any number. Majority voting over k=3 removes most stochastic flips at low cost. If the three passes disagree on a check, that check is borderline — keep the majority verdict and note it; persistent disagreement means the check wording is ambiguous (sharpen it in the baseline, see Calibration).

---
