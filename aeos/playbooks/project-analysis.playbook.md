# Playbook: Project Analysis

## Objective

Analyze a project or ecosystem and generate a factual, evidence-based technical map.

## Preconditions

- Workspace path exists.
- Read-only filesystem MCP is available.
- Global rules LCP is loaded.
- Security governance LCP is loaded.

## Agents

- Root Agent
- Architect Agent
- Security Agent
- Judge Agent

## Skills

- repo-scanner
- architecture-mapper
- security-audit

## MCPs

- filesystem-readonly
- git-readonly

## Steps

1. Load aeos.config.yaml.
2. Load registries.
3. Load global LCPs.
4. Validate permissions.
5. Scan repository structure.
6. Detect languages and build tools.
7. Detect frameworks.
8. Detect Docker and CI/CD files.
9. Detect tests.
10. Detect likely secrets without exposing values.
11. Generate ecosystem-map.md.
12. Generate risk-report.md.
13. Generate recommended-playbooks.md.
14. Send outputs to Judge Agent.
15. Generate judge-report.md.

## Blocking Conditions

- Missing evidence.
- Secret values printed.
- Unsupported destructive command attempted.
- Report contains unsupported claims.

## Outputs

- .aeos/ecosystem-map.md
- .aeos/risk-report.md
- .aeos/recommended-playbooks.md
- .aeos/judge-report.md
