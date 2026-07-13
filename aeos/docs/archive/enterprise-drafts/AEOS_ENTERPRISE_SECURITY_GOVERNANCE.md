# AEOS Enterprise Security Governance

## Security Baseline

AEOS aligns with enterprise AI/application security principles:

- prompt injection defense;
- insecure output handling prevention;
- training/data poisoning awareness;
- model DoS budgeting;
- supply-chain controls;
- sensitive information disclosure prevention;
- excessive agency prevention;
- overreliance prevention;
- secrets redaction;
- artifact integrity;
- auditable approvals.

## Production Controls

```text
Deny-All Permissions
Policy Fail-Closed
Tool Router Mandatory
MCP Allowlist
Secrets Never Persisted
Redaction Always On
Evidence Hash Chain
Package Verification
Approval Expiration
No Wildcard Approvals
No Direct Active Pack Import
No Auto-Merge
No Auto-Deploy
```

## Required Security Reports

```text
security-risk-report.md
secret-redaction-report.md
supply-chain-risk-report.md
mcp-risk-report.md
agent-scope-risk-report.md
package-trust-report.md
approval-audit-report.md
```

## Enterprise Blockers

AEOS must block when:

- secret is exposed;
- policy is bypassed;
- Tool Router is bypassed;
- direct MCP call is detected;
- approval is missing/expired/wildcard;
- package checksum fails;
- SLSA-like provenance is missing for release artifacts;
- untrusted pack is activated;
- high-risk agent task lacks review;
- LLM Judge tries to override deterministic failure.
