# AEOS v0.9 — Advanced Approval Gateway

## Mission

Turn approvals into explicit, granular, auditable authorization artifacts.

## Approval Types

```text
sandbox_write
patch_apply
test_run
git_commit
git_pr_create
package_extract
pack_import
mcp_enable
high_risk_task
```

## Approval Record

```yaml
approval:
  id:
  execution_id:
  action:
  scope:
  approved_by:
  reason:
  created_at:
  expires_at:
  constraints:
    max_files:
    allowed_paths:
    denied_paths:
    required_judge_status:
    required_evidence_verify:
  signature:
    type: local-hash
    value:
```

## CLI

```powershell
aeos approvals list --target <path>
aeos approval show <approval_id> --target <path>
aeos approve <execution_id> --target <path> --action patch.apply --scope "src/test/**" --expires-in 2h --reason "Apply generated tests only"
aeos deny <execution_id> --target <path> --reason "Scope too broad"
aeos approval revoke <approval_id> --target <path> --reason "Risk changed"
```

## Rules

- approvals expire;
- approvals are scoped;
- global wildcard approval is forbidden;
- approval cannot bypass policy;
- approval cannot authorize forbidden action;
- revoked approvals block execution;
- approval audit is immutable.
