# Recursive CI Recovery

## State model

Each recovery cycle records:

```json
{
  "cycle_id": "",
  "head_sha": "",
  "workflow_runs": [],
  "job_failures": [],
  "failure_fingerprints": [],
  "root_cause_groups": [],
  "patches": [],
  "verification": {},
  "commit_sha": null,
  "push_result": null,
  "progress": "POSITIVE|NONE|OSCILLATING|BLOCKED"
}
```

## Discovery

Discover all relevant workflow runs/checks for the current head SHA, including matrix children, reusable workflows and runs triggered by prior workflows. Continue discovery until the configured quiet period elapses without a new relevant run.

## Guardian coverage

- one `WorkflowGuardianLens` per workflow run;
- one `JobGuardianWorkUnit` per job or matrix child;
- guardians track status, conclusion, required/non-required classification and evidence refs;
- guardians never mutate the repository directly.

## Failure pipeline

`redact -> extract failing step -> normalize stack/error -> fingerprint -> correlate with recent diff -> group root causes -> select specialist lens -> reproduce -> plan -> patch -> verify`.

Equivalent fingerprints must be repaired once and revalidated across all affected jobs.

## Recursive controller

Defaults:

```yaml
max_cycles: 10
max_cycles_per_root_cause: 3
max_total_commits: 20
max_commits_per_cycle: 3
max_same_fingerprint_repetitions: 2
poll_interval_seconds: 30
monitor_timeout_minutes: 180
discovery_quiet_period_seconds: 60
parallel_limit: 8
```

Parallelize independent analysis only. Serialize patches that touch the same workflow, lockfile, config or source path.

## Progress detector

Positive progress includes fewer failing jobs, resolved fingerprints, a newly successful required check, or advancement past the previous blocking stage.

No progress includes same fingerprint/stack/path after a corrective cycle, alternating failures, new commits without improved pipeline state, or a repair that reintroduces a previously resolved root cause.

## Retry semantics

Use rerun without code changes only for failures classified as transient/retryable with evidence (for example runner/network/platform flake). Deterministic code/config/test failures require root-cause repair before rerun.

Never repeatedly rerun deterministic failures hoping for green.

## Human-only blockers

Do not auto-repair missing secret values, expired credentials without an authorized secret provider, billing failures, GitHub outages, required human reviewers, protected environment approvals, destructive migrations, clinical/regulatory approvals or missing PAT scope.

## Terminal states

- `PASS`: latest SHA is stable and all required workflows/jobs/checks are successful.
- `BLOCKED`: deterministic stop condition or human-only requirement.
- `REVIEW`: repair is ready but mutation/merge approval is required.
- `TIMEOUT`: monitor time budget exhausted.
