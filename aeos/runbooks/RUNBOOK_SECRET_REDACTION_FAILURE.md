# RUNBOOK_SECRET_REDACTION_FAILURE

## Purpose

Operational runbook for `RUNBOOK_SECRET_REDACTION_FAILURE`.

## First Response

1. Stop unsafe execution.
2. Preserve evidence.
3. Run `aeos evidence verify`.
4. Run relevant audit playbook.
5. Inspect Judge report.
6. Identify blocking condition.
7. Apply correction through sandbox/patch proposal.
8. Re-run Judge.

## Never Do

- bypass policy;
- delete evidence;
- hide failure;
- persist secrets;
- approve wildcard scope;
- mutate production;
- merge automatically.
