# Skill: kinghost-admin-supervisor

## Mission
Administer authorized KingHost environments end to end through the governed KingHost MCP, from access intake to remote inspection, controlled mutation, verification and rollback.

## Activates When
The request asks to manage KingHost hosting, domains, DNS, SSL, FTP/SFTP/SSH, databases, WordPress/PHP, deployments, logs, backups, performance, product/catalog data or workspace-to-host changes through AEOS.

## Uses MCP
- kinghost-commerce

## Access Contract
Access means operator-authorized, least-privilege, runtime-only credentials or approved secret references. This skill may guide the operator to supply credentials, validate host identity, open an opaque session and close it after work. It must never discover, extract, dump, scrape, brute-force, infer, persist or print credentials, cookies, tokens, session values or private keys.

## Administration Scope
- Access intake and session planning through `kinghost.access.request_plan`.
- Environment inventory through `kinghost.inspect_environment`.
- File operations through scoped SFTP actions.
- Read-only diagnostics through allowlisted SSH commands.
- Database reads and approved reversible mutations through database actions.
- Deployment, database, DNS and performance plans through read-only planning actions.
- CDC workspace operations as change-diff-control through `kinghost.cdc.workspace_plan`.

## CDC Workspace Workflow
Treat CDC as change-diff-control, not credential discovery. Capture remote state, compare it with workspace artifacts, generate a bounded diff, dry-run the change, apply only approved scoped mutations, verify post-state and preserve rollback evidence.

## Allowed Actions
- Produce an access plan that lists required credentials without storing them.
- Open governed sessions only after explicit authorization and host identity validation.
- Inventory files, runtime, logs, CMS, database and resource constraints.
- Generate deployment/database/DNS/catalog/performance plans from actual evidence.
- Apply production mutations only through approved MCP actions with `approved=true`, `change_id`, dry-run evidence and rollback reference.
- Close sessions and redact all evidence before reporting.

## Forbidden Actions
- Credential harvesting, cookie extraction, session dumping, brute force, credential stuffing or secret scanning for access.
- Storing credentials in Git, reports, memory, prompts, logs, SQL files, PHP files or evidence.
- Unrestricted shell, unscoped deletion, blind SQL, destructive DNS/database changes or provider-private API automation.
- Treating planning output as successful mutation.

## Required Inputs
- target_site_or_account
- authorization_context
- requested_outcome
- access_method: runtime_credentials|secret_reference|official_short_lived_token
- scope_root or equivalent bounded target scope
- risk_level
- rollback_strategy

## Output Schema
```json
{"status":"PASS|WARN|BLOCKED","access_plan":{},"environment":{},"change_set":[],"cdc":{},"verification":[],"rollback":[],"evidence_refs":[],"approval_required":true}
```

## Quality Gates
- Authorization and target scope are explicit.
- Credentials remain runtime-only and redacted.
- Host identity/TLS posture is validated before session use.
- Every mutation has pre-state, dry-run, approval, rollback and post-state verification.
- Database work is read-first and EXPLAIN-first where applicable.
- CDC compares hashes/state rather than trusting assumptions.
- Sessions are closed after the operation.

## Stop Conditions
Requested access depends on credential discovery or cookie/session extraction; target ownership is unclear; host identity cannot be validated; mutation lacks approval, dry-run, rollback or bounded scope; official provider capability is unknown for the requested operation.