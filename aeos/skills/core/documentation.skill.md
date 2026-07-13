# Skill: documentation

## Mission

Generate evidence-based documentation in sandbox.

## Allowed Actions

- Read authorized files through Tool Router.
- Request `complete-docs` MCP through Skill Executor and Tool Router.
- Generate reports in `.aeos/reports`.
- Generate evidence in `.aeos/evidence`.
- Generate sandbox artifacts when permitted.
- Never bypass permissions.

## Forbidden Actions

- Direct filesystem access.
- Direct Git mutation.
- Secret value exposure.
- Destructive shell.
- Unapproved writes outside `.aeos`.
- Unsupported factual claims.
- Silent failure.

## Required Evidence

- files inspected
- tool calls
- permission decisions
- generated artifacts
- risk classification
- Judge input when applicable
- documentation plan from `docs.plan`, `docs.package` or `docs.architecture_package`
- Mermaid diagrams generated or validated through `docs.mermaid_template` / `docs.validate_mermaid`
- ADR candidates when architecture or cloud readiness decisions are documented
- cloud readiness scorecard when deployment maturity is part of the request

## Prompt Contract

- State the objective, target scope, assumptions and constraints before execution.
- Use only evidence-backed facts; mark uncertainty explicitly.
- Route tool access through approved command, MCP or Tool Router paths.
- Redact secrets, credentials, tokens and sensitive values.
- Return facts, assumptions, risks, recommendations, evidence_refs and blocking_conditions when applicable.
- Stop when required evidence, permissions, policy approval or input context is missing.

## Complete Documentation Workflow

Use this workflow only when the user asks for complete, architectural, onboarding, operational or system documentation.

1. Inspect authorized repository evidence before making architecture claims.
2. Call `complete-docs` with `docs.plan` or `docs.package` to define required sections, evidence and diagrams.
3. Call `docs.architecture_package` when the request asks for complete architecture documentation, AI workspace engineering, cloud maturity or deployment readiness.
4. Generate Mermaid diagrams for architecture, runtime flow, skill/MCP/LSP routing, dependencies and cloud readiness when the requested documentation is complete.
5. Validate every Mermaid block with `docs.validate_mermaid` before finalizing.
6. Include README, architecture, runtime flow, skills/MCPs/LSPs, cloud readiness and ADR artifacts when using the architecture package workflow.
7. Keep diagrams compact; split large graphs by concern instead of producing unreadable diagrams.
8. Place generated documentation only in approved report or sandbox locations.

## Mermaid Rules

- Use Mermaid for topology, runtime flow, state, dependencies, deployment and data relationships.
- Every diagram must have a short explanation and evidence refs.
- Do not include secrets, credentials, tokens, hostnames or sensitive values in diagrams.
- Mark inferred nodes or relationships as assumptions.
- Return `REVIEW` when a diagram is useful but not fully evidence-backed.

## Architecture Package Rules

- Produce `README.md`, `docs/ARCHITECTURE.md`, `docs/RUNTIME_FLOW.md`, `docs/SKILLS_MCPS_LSPS.md`, `docs/CLOUD_READINESS.md` and ADR candidates for complete architecture packages.
- Treat cloud readiness as a gated review, not as a deployment approval.
- Mark every readiness dimension as `PASS`, `REVIEW` or `BLOCKED` from evidence only.
- Require ADR candidates for architecture, runtime, Tool Router, MCP, LSP, security or deployment decisions.
- Stop with `REVIEW` when the package can be generated but maturity evidence is incomplete.

## Quality Gates

- Facts cite evidence.
- Assumptions are explicitly marked.
- Risks are classified.
- Outputs follow schema.
- No secrets are printed.
- Required artifacts are hashed.
- Complete documentation includes validated Mermaid diagrams unless explicitly out of scope.
- Architecture packages include ADR candidates and cloud readiness gates.
