# Playbook: parallel-execution-smoke-test

## Objective

Validate safe parallel execution without mutating project files.

## Steps

1. Load parallel execution config.
2. Build a task DAG with independent read-only tasks.
3. Compute read_set/write_set for each task.
4. Run Conflict Detector.
5. Execute safe read-only tasks in parallel.
6. Preserve deterministic result ordering.
7. Generate parallel execution report.
8. Run Judge.

## Outputs

- `.aeos/evidence/{execution_id}/parallel-task-graph.json`
- `.aeos/evidence/{execution_id}/conflict-report.json`
- `.aeos/reports/{execution_id}/parallel-execution-report.md`

## Blocking Conditions

- missing read/write set;
- conflict unresolved;
- non-deterministic ordering;
- missing task result;
- hash-chain gap.
