# Playbook: Documentation Generation

## Objective

Generate comprehensive documentation for a project including architecture decisions, API docs, and runbooks.

## Preconditions

- Workspace path exists.
- Read-only and sandbox-write MCPs available.
- Global rules and documentation-standards LCPs loaded.

## Agents

- Documenter Agent
- Architect Agent
- Judge Agent

## Skills

- documentation
- architecture-mapper

## MCPs

- filesystem-readonly
- filesystem-write-sandbox

## Steps

1. Load project context and existing documentation.
2. Scan repository structure and map architecture.
3. Identify public APIs, modules, and entry points.
4. Generate Architecture Decision Records (ADRs) for key patterns.
5. Generate module-level documentation.
6. Generate API reference documentation.
7. Generate runbook for common operations.
8. Validate documentation against standards LCP.
9. Send outputs to Judge Agent.
10. Generate judge-report.md.

## Blocking Conditions

- No architecture map generated.
- Documentation does not match actual code.
- Missing ADR for documented decisions.
- Incomplete coverage of public APIs.

## Outputs

- .aeos/docs/architecture.md
- .aeos/docs/adr/*.md
- .aeos/docs/api-reference.md
- .aeos/docs/runbook.md
- .aeos/judge-report.md
