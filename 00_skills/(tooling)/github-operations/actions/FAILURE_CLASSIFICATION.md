# GitHub Actions Failure Classification

Normalize failures before reasoning. Redact credentials first, then extract only the failing step/stack/error needed for root-cause analysis.

## Categories

- workflow_syntax
- permissions
- authentication
- secret_missing
- secret_exposure
- dependency_conflict
- compilation
- unit_test
- integration_test
- smoke_test
- e2e_test
- flaky_test
- timeout
- resource_exhaustion
- docker_build
- package_publish
- artifact_upload
- cache_failure
- matrix_failure
- reusable_workflow
- branch_protection
- environment_configuration
- infrastructure_validation
- security_scan
- quality_gate
- external_service
- github_platform
- unknown

## Failure record

```json
{
  "failure_id": "",
  "workflow_run_id": "",
  "job_id": "",
  "step_name": "",
  "category": "",
  "fingerprint": "",
  "summary": "",
  "root_cause_hypothesis": "",
  "confidence": 0.0,
  "specialist_lens": "",
  "evidence_refs": [],
  "retryable": false,
  "code_change_required": false,
  "human_action_required": false
}
```

## Root-cause grouping

Group equal normalized fingerprints before repair. Matrix jobs failing for one dependency/workflow/config cause produce one repair plan and one coordinated patch, then all affected jobs are revalidated.

A transient retry must be evidence-backed. Deterministic failures are not repeatedly rerun without a repair.
