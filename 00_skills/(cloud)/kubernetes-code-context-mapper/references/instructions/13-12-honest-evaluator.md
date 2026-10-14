<!-- Package: 00_skills/(cloud)/kubernetes-code-context-mapper; relative command/resource examples resolve from that package or workspace root. -->

## 12. Honest evaluator

Before completion, apply `evaluation/HONEST_EVALUATOR.md`.

The evaluator must reject:

- pod-to-code mapping based only on a name similarity;
- label-only ownership when selector or owner-reference evidence is missing;
- unredacted config or secret material;
- missing test and remediation boundaries;
- cluster health claims based only on pod phase.
