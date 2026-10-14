# GitHub Actions Recursive Recovery

## Recovery segment

`DISCOVER -> MONITOR -> CLASSIFY -> GROUP -> REPRODUCE -> PLAN -> PATCH -> VERIFY -> JUDGE -> COMMIT -> AUTHORIZED_PUSH -> REDISCOVER`

Only the recovery segment repeats. Previous-SHA CI evidence is invalid after each push.

## Default bounds

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

## Progress

Progress is measurable reduction/resolution of active failure fingerprints/jobs, newly successful required checks, or deterministic advancement past the previous blocker. Creating another commit alone is not progress.

Stop on repeated no-progress fingerprint, oscillation, cycle/time/token exhaustion or a human-only blocker.

## Retry-only cases

Rerun without code/config change only when evidence classifies the failure as transient/retryable (runner/platform/network flake). Deterministic failures require root-cause repair first.

## Final gate

PASS requires a stable latest SHA after the discovery quiet period with every required run/job/check terminal and successful plus Judge/Evidence/security gates.
