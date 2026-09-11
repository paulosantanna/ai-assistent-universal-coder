# GitHub Actions Monitoring

Owned by `codenavi-agent`; workflow/job guardians are bounded lenses/work units, not agents.

## Coverage

For the current head SHA, discover and track all relevant:

- workflow runs and rerun attempts;
- jobs and matrix children;
- reusable/dependent workflows;
- check suites/check runs visible through repository policy;
- runs created after a corrective push.

Do not stop after the first workflow. Continue discovery until the configured quiet period elapses with no new relevant run.

## State

Track `queued`, `requested`, `waiting`, `pending`, `in_progress`, `completed` plus conclusions including `success`, `failure`, `cancelled`, `timed_out`, `action_required`, `neutral`, `skipped`, `stale` and `startup_failure`.

A required check is successful only when it belongs to the latest SHA and its terminal conclusion is `success`. `neutral`/`skipped` require explicit non-required classification.

## Freshness

A corrective push changes the head SHA and invalidates previous-SHA success evidence. Re-discover the complete relevant run/check set for the new SHA.

## Polling defaults

- interval: 30 seconds;
- total monitoring budget: 180 minutes;
- discovery quiet period: 60 seconds.

Polling is state-driven and stops immediately on permanent deny/human-only blocker. It must not create a background process outside the governed execution.
