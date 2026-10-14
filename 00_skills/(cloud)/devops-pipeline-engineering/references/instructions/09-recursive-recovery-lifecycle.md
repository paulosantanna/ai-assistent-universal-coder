<!-- Package: 00_skills/(cloud)/devops-pipeline-engineering; relative command/resource examples resolve from that package or workspace root. -->

## Recursive recovery lifecycle

`DISCOVER -> MONITOR -> CLASSIFY -> GROUP_ROOT_CAUSES -> REPRODUCE -> PLAN -> PATCH -> VERIFY_LOCAL -> JUDGE -> COMMIT -> AUTHORIZED_PUSH -> REDISCOVER`

Repeat only the recovery segment. Do not rerun unrelated setup work blindly.

Default limits:

```yaml
max_cycles: 10
max_cycles_per_root_cause: 3
max_total_commits: 20
max_commits_per_cycle: 3
max_same_fingerprint_repetitions: 2
poll_interval_seconds: 30
monitor_timeout_minutes: 180
discovery_quiet_period_seconds: 60
parallel_failure_analysis: true
parallel_limit: 8
serialize_overlapping_files: true
require_progress: true
stop_on_oscillation: true
```

Stop with `BLOCKED` on cycle exhaustion, repeated no-progress fingerprints, oscillation, missing secret value, insufficient PAT scope, external/GitHub outage, required human reviewer/environment approval, destructive migration, unauthorized deploy or any permanent deny.
