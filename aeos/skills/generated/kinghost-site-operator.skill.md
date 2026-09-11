# Skill: kinghost-site-operator

## Mission
Operate and evolve websites hosted at KingHost using evidence-first inspection, reversible plans and least privilege.

## Activates When
KingHost hosting, DNS, SSL, FTP/SFTP/SSH, Git publication, databases, WordPress/CMS, Node/PHP runtime, server/site troubleshooting, deployment or hosting performance is requested.

## Does Not Activate When
The target is unrelated to KingHost or the request requires an undocumented/private provider API.

## Allowed Actions
- Inventory the actual hosting plan, runtime, domains, DNS, SSL, databases, application stack and limits.
- Diagnose logs, HTTP errors, resource pressure and deployment constraints.
- Plan FTP/SFTP/SSH/Git deployments with backup, health checks and rollback.
- Plan database queries, EXPLAIN analysis, indexes, migrations and read-safe diagnostics.
- Plan DNS/SSL changes and validate propagation strategy.
- Consult current official KingHost documentation before material decisions.
- Route broad administration requests to `kinghost-admin-supervisor` when access intake, environment inventory, mutation and verification must be coordinated.

## Forbidden Actions
- Store or print passwords, tokens, SSH private keys or database credentials.
- Discover, extract or scrape credentials from cookies, saved sessions, files or browser state.
- Assume plan capabilities not proven by evidence.
- Execute unrestricted shell, destructive SQL, DNS mutation or production deployment by default.
- Bypass Judge, approval, dry-run, backup or rollback requirements.

## Required Inputs
- target_site_or_domain
- requested_outcome
- environment_evidence
- risk_level

## Output Schema
```json
{"status":"PASS|WARN|BLOCKED","environment":{},"plan":[],"risks":[],"rollback":[],"evidence_refs":[],"approval_required":false}
```

## Quality Gates
- Current official documentation for provider-specific facts.
- Actual plan/runtime constraints identified or explicitly marked unknown.
- Every mutation has precondition, verification and rollback.
- Database work is explain-first and destructive operations are blocked by default.
- Secrets are redacted.

## Stop Conditions
Missing authoritative evidence; unknown mutation target; missing rollback; credentials exposed; undocumented capability required.