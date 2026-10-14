# Domain procedure

Inputs: Authorized target, threat scope, repository/configuration and available defensive tools.

Outputs: Prioritized findings with file/config pointers, confidence, impact, mitigation and verification plan.

1. Map entrypoints, identities, data flows and external trust boundaries.
2. Inspect authorization, input validation, secret handling, dependencies and deployment controls relevant to the scope.
3. Use available defensive checks only within authorization; record their actual results.
4. Separate confirmed findings from hypotheses and produce actionable mitigations without exposing secret values.

Verification: apply the supplied domain contract to actual outputs; record source/version and executed check results. Missing required evidence, interface or permission blocks its dependent step. AGENTS.md governs; no independent agent identity or runtime installation is implied.
