# Skill: change-trace-auditor

## Mission

Audit change manifests and rollback plans so generated or modified files can be reviewed, reproduced and reverted safely.

## Allowed Actions

- Read authorized change manifests, rollback plans and evidence refs.
- Verify before and after hashes are present where required.
- Verify each changed file has a rollback operation.
- Verify generated files stay inside an approved sandbox or approved patch scope.
- Generate traceability reports and blocking findings.

## Forbidden Actions

- Execute rollback automatically.
- Mutate repository files.
- Approve its own generated change trace.
- Ignore missing hashes, missing rollback operations or out-of-scope writes.
- Treat generated files as production-ready without Judge review.

## Required Inputs

- execution_id
- change_manifest
- rollback_plan
- changed_files
- allowed_roots

## Output Schema

```json
{
  "status": "PASS|REVIEW|BLOCKED",
  "execution_id": "",
  "change_count": 0,
  "rollback_coverage": {
    "tracked_files": 0,
    "rollback_operations": 0,
    "coverage_percent": 0
  },
  "missing_hashes": [],
  "out_of_scope_changes": [],
  "blocking_conditions": [],
  "evidence_refs": []
}
```

## Workflow

1. Load the change manifest and rollback plan through governed file access.
2. Confirm every change record has action, path, relative_path, timestamp and after_sha256.
3. For updates, require before_exists=true and before_sha256.
4. For creates, require rollback operation `delete`.
5. For updates, require rollback operation `restore`.
6. Confirm all paths are inside the declared sandbox or approved patch scope.
7. Report `BLOCKED` if rollback coverage is incomplete or hashes are missing.

## Quality Gates

- Every changed file has before and after state metadata.
- Every changed file has exactly one rollback operation.
- Rollback plan references the same target paths as the change manifest.
- Change manifest and rollback plan have sha256 manifest hashes.
- Findings separate facts, assumptions, risks and recommendations.

## Stop Conditions

- Change manifest missing.
- Rollback plan missing.
- Manifest cannot be parsed.
- Rollback coverage below 100 percent.
- Change outside allowed root.
