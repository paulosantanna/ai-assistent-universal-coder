# Domain procedure

Inputs: User outcome, inspected repository or greenfield constraints, architecture/language/database requirements.

Outputs: Reviewable blueprint, component/data-flow map, implementation sequence, risks and acceptance gates.

1. Inspect existing architecture and constraints before choosing patterns.
2. Map components, interfaces, persistence, authentication and trust boundaries to the requested outcome.
3. Specify deployment, observability and rollback requirements without executing deployment.
4. Sequence bounded work with dependencies and measurable acceptance checks; flag unresolved choices.

Verification: apply the supplied domain contract to actual outputs; record source/version and executed check results. Missing required evidence, interface or permission blocks its dependent step. AGENTS.md governs; no independent agent identity or runtime installation is implied.
