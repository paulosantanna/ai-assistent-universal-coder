# AEOS v0.95 — Security Hardening

## Mission

Harden AEOS before v1.0.

## Threats

```text
Prompt Injection
Tool Poisoning
MCP Tool Poisoning
Secret Leakage
Package Tampering
ZIP Path Traversal
Evidence Tampering
Approval Forgery
Policy Bypass
Agent Scope Creep
Cache Poisoning
Dependency Confusion
Supply Chain Risk
Unsafe Shell Execution
Browser Session Leakage
```

## Controls

- deny-all permissions;
- explicit capability allowlists;
- MCP allowlists;
- package quarantine;
- evidence integrity;
- hash-chain;
- approval expiration;
- no raw secret persistence;
- redaction;
- trust policy;
- dependency verification;
- import staging;
- Judge deterministic gates;
- audit immutability.

## Security Reports

```text
.aeos/reports/{execution_id}/threat-model.md
.aeos/reports/{execution_id}/security-hardening-report.md
.aeos/reports/{execution_id}/trust-policy-report.md
.aeos/reports/{execution_id}/package-quarantine-report.md
```
