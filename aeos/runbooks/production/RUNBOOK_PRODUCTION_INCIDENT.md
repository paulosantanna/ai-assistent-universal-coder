# RUNBOOK_PRODUCTION_INCIDENT

## Purpose

Triage, containment, rollback and postmortem for AEOS production incidents.

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
