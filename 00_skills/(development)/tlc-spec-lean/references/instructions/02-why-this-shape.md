<!-- Package: 00_skills/(development)/tlc-spec-lean; relative command/resource examples resolve from that package or workspace root. -->

## Why this shape

The dominant failure of a coding agent is not bad reasoning, it is a requirement that was read
and never became an active obligation - and then a completion claim on top of it. The
mitigation that measures well is a **small, frozen, external obligation set** plus a
**verifier that is not the author**; a self-check reproduces the author's own blind spot. So
this skill spends its budget on those two things and refuses to spend it on choreographing how
the model works.

Two consequences worth stating up front, because they are what make this different from a
conventional spec-driven flow:

- **Granularity is not quality.** Splitting a feature into fifteen one-file tasks buys
  ordering, not correctness, and it costs a re-read of the process on every task. Proof
  coverage buys correctness.
- **A plan the model must obey competes with the obligations for attention.** Fields like
  `Where`, `Tools`, `Depends on` are the model's job to decide, so they are not written down.
