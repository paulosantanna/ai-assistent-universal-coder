# Playbook: enterprise-security-audit

## Objective

Execute `enterprise-security-audit` under AEOS Enterprise governance.

## Required Runtime

- Kernel Runtime
- Permission Engine
- Policy Engine
- Tool Router
- MCP Gateway
- Agent Runtime
- Evidence Store
- Judge Layer

## Steps

1. Load AEOS config.
2. Load workbench profile.
3. Resolve LCPs.
4. Resolve skills.
5. Resolve MCPs.
6. Create task graph.
7. Run dry-run.
8. Validate permission/policy.
9. Execute only allowed read/sandbox operations.
10. Collect evidence.
11. Generate report.
12. Hash artifacts.
13. Run Judge.

## Blocking Conditions

- missing evidence;
- unsupported claim;
- raw secret exposure;
- permission denied;
- policy denied;
- direct tool bypass;
- missing Judge report;
- hash mismatch;
- unsafe package import;
- wildcard approval.

## Outputs

- `.aeos/evidence/{execution_id}/`
- `.aeos/reports/{execution_id}/enterprise-security-audit.md`
