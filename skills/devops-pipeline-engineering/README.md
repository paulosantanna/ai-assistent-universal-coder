# devops-pipeline-engineering

Governed AEOS skill for Git/GitHub CI/CD creation, monitoring, recursive repair and merge readiness.

## Important architecture rule

AEOS has one canonical agent identity: `codenavi-agent`. This skill does not create subagents. A user request for one worker per Action is implemented as isolated `WorkflowGuardianLens` / `JobGuardianWorkUnit` contexts owned by `codenavi-agent`, preserving one-agent governance while providing independent monitoring coverage.

## Typical flow

1. inspect repository/branch protection/workflows;
2. establish local test baseline;
3. create or harden CI;
4. commit/push through governed GitHub operations;
5. discover every relevant run/check for the new head SHA;
6. assign guardian contexts;
7. monitor all required runs/jobs;
8. fingerprint/group failures;
9. repair root causes with specialized lenses;
10. test locally, Judge, commit and push;
11. repeat until green or bounded stop condition;
12. revalidate latest SHA;
13. produce merge readiness decision;
14. optionally create Work Bundle artifacts.

## Pipeline success

Do not confuse API HTTP status with CI status. Pipeline success requires GitHub Actions/check conclusions for the latest SHA to satisfy repository-required policy.

## Safety

- repository deletion: permanently denied/manual-only;
- secret-value read/export: denied;
- PAT scope escalation: denied;
- force-push: denied by default;
- branch-protection bypass: denied;
- merge: approval-required by default;
- recursive retry: bounded by progress/time/token/cycle budgets.
