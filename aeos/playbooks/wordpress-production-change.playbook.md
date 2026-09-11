# Playbook: wordpress-production-change

## Objective

Apply an authorized WordPress change using the existing Beta baseline, current narrow evidence, current documentation, approval, rollback and deterministic verification.

## Required Agent

- `codenavi-agent` only.

## Required Skills

- `wordpress-expert`
- `security-audit`
- `rollback-planner`

## Required MCP

- `wordpress-expert`

## Steps

1. Load root governance and the requested site/objective.
2. Run `wordpress.site.map_status`.
3. If no Beta baseline exists, execute `wordpress-site-onboarding-beta` first.
4. Load the baseline with `wordpress.site.map_get`; never remap it automatically.
5. Inspect only current resources/routes relevant to the requested delta.
6. Retrieve current official WordPress documentation needed for the change; use Reddit only as secondary troubleshooting evidence.
7. For external APIs, retrieve current official provider documentation before proposing integration code.
8. Classify risk and create minimal change-set, backup/rollback and verification plan.
9. Run Front-end Staff self-review for visual/frontend work.
10. Obtain policy/permission/Judge/approval required for production mutation.
11. Open runtime write mode only for the approved execution.
12. Execute the smallest allowlisted WordPress MCP operation(s).
13. Re-read every changed remote resource.
14. For visual changes, validate rendered frontend, responsive states, accessibility and browser console/network when a governed browser/testing capability is available.
15. Verify integration behavior, cache effects, plugin/theme interaction and rollback readiness.
16. Record evidence, residual risk and debrief.

## Deletion

Use trash-first. Permanent content deletion additionally requires the permanent-delete runtime gate and literal confirmation. Do not expose generic filesystem/theme/plugin/database deletion.

## Terminal states

- `PASS`: requested remote change is verified.
- `REVIEW`: plan/evidence ready but approval is still required.
- `BLOCKED`: safety, documentation, authorization, capability, rollback or verification gate failed.
