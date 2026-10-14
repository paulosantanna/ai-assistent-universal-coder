<!-- Package: 00_skills/(development)/spec-driven; relative command/resource examples resolve from that package or workspace root. -->

## Deterministic gates

- Before confirming a spec: `<skill-dir>/scripts/validate_spec.py <spec-path-or-feature>`
- Before presenting tasks: `<skill-dir>/scripts/validate_tasks.py <tasks-path-or-feature>`
- On each authorized commit: `<skill-dir>/scripts/check_commit.py --message "<msg>"`
- Before declaring done: `<skill-dir>/scripts/validate_state.py <feature>`
- Confirmed lessons: `<skill-dir>/scripts/lessons.py list --status confirmed`

Skip a script only when no code-execution tool exists; then perform the same checks by reading the artifact and say once that the path is degraded.
