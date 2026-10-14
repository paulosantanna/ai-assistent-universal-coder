<!-- Package: 00_skills/(monitoring)/telemetry-bug-root-cause-solver; relative command/resource examples resolve from that package or workspace root. -->

## 5. Scope

### Included

- Build a failure timeline from logs, metrics, traces, alerts, events and CI output.
- Extract trace IDs, span IDs, request IDs, pod names, namespaces, deployment versions, commit SHAs and exception chains.
- Map runtime evidence to code, configuration, tests and ownership boundaries.
- Reproduce the defect with a failing test, focused command or deterministic evidence when technically possible.
- Propose or apply a minimal fix inside the authorized code scope.
- Run focused and risk-based verification.
- Produce rollback and learning records.

### Excluded

- Broad refactoring unrelated to the defect.
- Deploying to production.
- Changing alert thresholds to hide defects.
- Treating missing telemetry as proof of health.
- Storing secrets, customer data or protected data in memory.
