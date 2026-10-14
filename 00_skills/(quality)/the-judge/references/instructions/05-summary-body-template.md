<!-- Package: 00_skills/(quality)/the-judge; relative command/resource examples resolve from that package or workspace root. -->

## Summary Body Template

```markdown
## TL;DR
One to three sentences: what the PR does and the verdict with its reason. Must contain the verdict token (APPROVE, COMMENT, or REQUEST_CHANGES) verbatim; the gate checks for it.

## Findings
| ID | Severity | Location | Summary |
|---|---|---|---|

## Resolution (round 2+)
| ID | Status | Note |
|---|---|---|
Every previous finding appears here with status resolved (with the commit), open, or declined-accepted (author's reason held). Omit this section in round 1.

## Promote to lint rule
Findings in this review that are deterministic by nature (banned pattern, naming convention, style rule). For each: the rule, and a one-line sketch of how to lint it. Reviews should get cheaper every cycle; this section is the flywheel. Write "none" if empty.

## Research log
URLs consulted in Step 2, one per line, with the claim each one supports or refutes. Sources that refuted a candidate finding belong here too: a documented non-finding is evidence of diligence and saves a future round. Write "no external surfaces touched" if that is the case.

## Checks run
Deterministic ladder results from Step 1, verbatim numbers with no interpretation: test counts (passed/failed/skipped), linter and typechecker outcome, bypass scan candidate count.

## Skipped files
Mechanical/generated files excluded from review.

## Nit overflow
"N additional nits not posted individually" when the cap was hit. Omit otherwise.
```
