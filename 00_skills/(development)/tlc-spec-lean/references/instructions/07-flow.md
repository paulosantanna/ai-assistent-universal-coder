<!-- Package: 00_skills/(development)/tlc-spec-lean; relative command/resource examples resolve from that package or workspace root. -->

## Flow

**Plan** - the problem, then the path and what the change disturbs, then the rest of the shape,
then the criteria. Writing still goes problem → surfaces → criteria → shape. Facts you look
up; decisions you ask - and when you ask, concrete options with your recommendation, at most two
per turn. **Two enumerations do the finding**, because "consider the edge cases" finds nothing: the
surfaces this feature exposes, each carrying the same decisions every time it appears, and the nine
implicit-requirement dimensions. Both take a mandatory `n/a - <reason>`, so a blank is an item
nobody decided rather than one that does not apply. One artifact a human reads and objects to
before any check exists. Full process, how to ask, rules per shape section, template and closure
gate: [plan.md](../tlc/references/plan.md).

**Checks** - derive claims with proofs from the plan, join every enumerated set member to a check,
and record where each swept dimension landed. Close with `## Handoff` and the arithmetic; if
the estimate exceeds the budget, stop for the mechanism ask before Build. This is the artifact
everything downstream refers to by check number: [checks.md](../tlc/references/checks.md).

**Build** - your call how, after the `## Handoff` arithmetic and, if the estimate exceeds the
budget, the user's mechanism choice. Write the tests from the checks, implement, run each
proof, commit in coherent pieces. No task list, no per-task review tables. Boundaries,
`Landing` timing, handoff and the scope guardrail: [build.md](../tlc/references/build.md).

**Verify** - when the last commit of the feature lands, dispatch a fresh Verifier in the
same turn. Do not ask. Do not wait for "verify work". Procedure, report format and scoped
re-verification: [verify.md](../tlc/references/verify.md).

Durable memory - project decisions, session handoff, and the lessons layer:
[memory.md](../tlc/references/memory.md).
