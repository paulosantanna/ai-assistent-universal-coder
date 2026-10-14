<!-- Package: 00_skills/(tooling)/nx-ci-monitor; relative command/resource examples resolve from that package or workspace root. -->

## Example Session

### Example 1: Normal Flow with Self-Healing (medium verbosity)

```
[ci-monitor] Starting CI monitor for branch 'feature/add-auth'
[ci-monitor] Config: max-cycles=5, timeout=120m, verbosity=medium

[ci-monitor] Spawning subagent to poll CI status...
[CI Monitor] CI attempt: IN_PROGRESS | Self-Healing: NOT_STARTED | Elapsed: 1m
[CI Monitor] CI attempt: FAILED | Self-Healing: IN_PROGRESS | Elapsed: 3m
[CI Monitor] CI attempt: FAILED | Self-Healing: COMPLETED | Elapsed: 5m

[ci-monitor] Fix available! Verification: COMPLETED
[ci-monitor] Applying fix via MCP...
[ci-monitor] Fix applied in CI. Waiting for new CI attempt...

[ci-monitor] Spawning subagent to poll CI status...
[CI Monitor] New CI attempt detected!
[CI Monitor] CI attempt: SUCCEEDED | Elapsed: 8m

[ci-monitor] CI passed successfully!

[ci-monitor] Summary:
  - Total cycles: 2
  - Total time: 12m 34s
  - Fixes applied: 1
  - Result: SUCCESS
```

### Example 2: Pre-CI Failure (medium verbosity)

```
[ci-monitor] Starting CI monitor for branch 'feature/add-products'
[ci-monitor] Config: max-cycles=5, timeout=120m, auto-fix-workflow=true

[ci-monitor] Spawning subagent to poll CI status...
[CI Monitor] CI attempt: FAILED | Self-Healing: COMPLETED | Elapsed: 2m

[ci-monitor] Applying fix locally, enhancing, and pushing...
[ci-monitor] Committed: abc1234

[ci-monitor] Spawning subagent to poll CI status...
[CI Monitor] Waiting for new CI attempt... (expected SHA: abc1234)
[CI Monitor] ⚠️  CI attempt timeout (10 min). Returning no_new_cipe.

[ci-monitor] Status: no_new_cipe
[ci-monitor] --auto-fix-workflow enabled. Attempting lockfile update...
[ci-monitor] Lockfile updated. Committed: def5678

[ci-monitor] Spawning subagent to poll CI status...
[CI Monitor] New CI attempt detected!
[CI Monitor] CI attempt: SUCCEEDED | Elapsed: 18m

[ci-monitor] CI passed successfully!

[ci-monitor] Summary:
  - Total cycles: 3
  - Total time: 22m 15s
  - Fixes applied: 1 (self-healing) + 1 (lockfile)
  - Result: SUCCESS
```
