# Domain procedure

Inputs: Task domain, inspected profile definitions, available MCP/LSP/tools and permission constraints.

Outputs: Selected profile, capability/resource set, rationale, exclusions and missing prerequisites.

1. Read actual profile definitions and the task requirements before selection.
2. Match language/domain/runtime requirements to observed capabilities.
3. Exclude unavailable or incompatible components and preserve permission/secret boundaries.
4. Return a deterministic selection with evidence; unresolved prerequisites block dependent operations rather than inventing tools or activating everything.

Verification: apply the supplied domain contract to actual outputs; record source/version and executed check results. Missing required evidence, interface or permission blocks its dependent step. AGENTS.md governs; no independent agent identity or runtime installation is implied.
