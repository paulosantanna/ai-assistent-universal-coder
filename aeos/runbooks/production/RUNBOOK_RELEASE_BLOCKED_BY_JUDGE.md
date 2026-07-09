# RUNBOOK_RELEASE_BLOCKED_BY_JUDGE

## Purpose

Handle release blocked by deterministic Judge.

## Immediate Actions

1. Stop unsafe execution.
2. Preserve evidence.
3. Run `aeos evidence verify`.
4. Run relevant enterprise playbook.
5. Inspect Judge report.
6. Create incident record.
7. Apply fix through sandbox/patch workflow.
8. Re-run Judge.

## Never

- delete evidence;
- hide failed checks;
- bypass policy;
- expose secrets;
- approve wildcard scope;
- auto-merge;
- auto-deploy.
