# Playbook: Security Secrets Audit

## Objective

Scan a repository for exposed secrets, credentials, tokens, and sensitive configuration without reading their values.

## Preconditions

- Workspace path exists.
- Read-only filesystem and git MCPs available.
- Security governance LCP loaded.

## Agents

- Security Agent
- Judge Agent

## Skills

- security-audit

## MCPs

- filesystem-readonly
- git-readonly

## Steps

1. Load security governance LCP.
2. Scan entire repository for secret patterns.
3. Scan git history for committed secrets.
4. Scan configuration files for credential patterns.
5. Check .gitignore and .dockerignore for coverage gaps.
6. Scan CI/CD pipeline definitions for embedded secrets.
7. Generate secrets audit report without exposing values.
8. Classify findings by severity.
9. Recommend remediation actions.
10. Send outputs to Judge Agent.
11. Generate judge-report.md.

## Blocking Conditions

- Secret values printed or logged.
- Audit report contains plaintext secrets.
- Critical severity secrets found without remediation plan.
- Missing evidence of scan coverage.

## Outputs

- .aeos/secrets-audit-report.md
- .aeos/secrets-evidence-index.md
- .aeos/remediation-recommendations.md
- .aeos/judge-report.md
