# Runbook — Parallel Execution Failure

## Symptoms

- conflict report blocks execution;
- missing read/write set;
- hash-chain gap;
- non-deterministic output order.

## Actions

1. Stop parallel execution.
2. Inspect conflict-report.json.
3. Serialize conflicting steps.
4. Re-run dry-run.
5. Re-run Judge.
6. Update playbook read_set/write_set.
