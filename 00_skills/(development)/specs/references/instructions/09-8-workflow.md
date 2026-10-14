<!-- Package: 00_skills/(development)/specs; relative command/resource examples resolve from that package or workspace root. -->

## 8. Workflow

1. State the objective, target scope, downstream skill, assumptions and constraints.
2. Inspect only the repository context needed to understand the affected artifact class.
3. Load relevant negative knowledge before proposing an approach.
4. Create or refine requirements before design; use EARS-style statements when event-driven behavior is present.
5. Link each acceptance criterion to one or more requirements and to an explicit verification method.
6. Create design notes only after requirements are coherent enough to test.
7. Generate tasks that are discrete, dependency-aware and verifiable.
8. Build a test applicability matrix for the exact change risk, marking each category `REQUIRED`, `NOT_APPLICABLE` or `DEFERRED_WITH_APPROVED_RISK`.
9. Define evidence gates, approval gates, rollback expectations and stop conditions.
10. Validate the package against `schemas/output.schema.json` when a machine-readable package is produced.
11. Return `PASS` only when the spec is sufficient for downstream execution, `REVIEW` when human judgment is needed, and `BLOCKED` when required context, evidence or approval is missing.
