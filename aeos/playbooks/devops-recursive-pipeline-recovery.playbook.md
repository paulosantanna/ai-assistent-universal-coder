# Playbook: devops-recursive-pipeline-recovery

## Objective

Create or repair GitHub Actions CI/CD, monitor every required run/job/check for the latest head SHA, recursively repair root causes under bounded governance, and produce merge readiness only after the pipeline is fully green.

## Required Agent

- `codenavi-agent` only.

## Required Skills

- `devops-pipeline-engineering`
- `security-audit`
- `rollback-planner`
- `token-budget-manager`, when available

## Required Context

- repository path/name;
- target branch and current head SHA;
- pull request number when applicable;
- repository-required checks/branch protection;
- runtime-only GitHub credential reference;
- user authorization scope for push/merge.

## Steps

1. Load root `AGENT.md` and relevant `.notebook` continuity state.
2. Validate registries, policy and permission contracts.
3. Inspect repository, branch protection, workflows and package/test toolchains.
4. Establish local baseline tests and current head SHA.
5. Create/harden workflows only when required by the mission.
6. Run focused local verification and secret scan.
7. Create a selective, atomic commit and authorized push when mutation is permitted.
8. Discover every relevant workflow run/check for the new head SHA.
9. Allocate one `WorkflowGuardianLens` per run and one bounded job work unit per job/matrix child.
10. Monitor until terminal state or an actionable failure becomes available.
11. Redact logs; classify and fingerprint failures.
12. Group equivalent failures by root cause.
13. Select the smallest specialized lens for each root-cause group.
14. Reproduce locally when feasible.
15. Run Chief/Staff self-review; block `REJECTED`, revise `NEEDS_REWORK`.
16. Generate a minimal recovery plan with verification and rollback.
17. Apply controlled repair only within authorized scope.
18. Run focused tests, regression checks, secret scan and Judge.
19. Create atomic corrective commit and authorized push.
20. Invalidate all prior-SHA CI evidence.
21. Re-discover runs/checks for the new SHA.
22. Repeat steps 8–21 while progress exists and cycle/time/token limits remain.
23. Require a discovery quiet period with no new relevant runs.
24. Verify all required workflows/jobs/checks are successful on the latest SHA.
25. Produce merge readiness decision.
26. Execute merge only when explicitly authorized for the current execution and all gates remain valid.
27. Finalize evidence and optional Work Bundle artifacts.
28. Refresh handoff/progress with the final verified state.

## Recursive Limits

- max cycles: 10
- max cycles per root cause: 3
- max total corrective commits: 20
- max commits per cycle: 3
- same fingerprint without progress: 2
- monitor timeout: 180 minutes
- discovery quiet period: 60 seconds

## Blocking Conditions

- repository deletion requested;
- secret value required or exposed;
- PAT scope insufficient;
- branch protection requires a human action;
- workflow/environment requires human approval;
- GitHub/platform outage;
- external service failure outside repository control;
- repeated failure without progress;
- recovery oscillation;
- cycle/token/time limit reached;
- destructive migration or deployment outside explicit authorization;
- Judge or Evidence Verify failure;
- any required check unsuccessful on the latest SHA.

## Anti-cheating Controls

Do not obtain green CI by:

- deleting tests;
- arbitrary skip/xfail;
- `continue-on-error` for a required job;
- weakening assertions/coverage/security gates;
- removing required checks;
- silencing exceptions;
- inventing or hardcoding credentials;
- force-pushing around protection.

## Outputs

- `.aeos/evidence/{execution_id}/devops-recursive-recovery-summary.json`
- `.aeos/evidence/{execution_id}/devops-final-pipeline-status.json`
- `.aeos/evidence/{execution_id}/devops-merge-decision.json`
- `.aeos/reports/{execution_id}/devops-operation-report.md`
- `.aeos/reports/{execution_id}/devops-token-budget-report.md`
- optional verified Git bundle + SHA256 + import/rollback plan

## Terminal States

- `PASS`: all required latest-SHA checks green and governance gates pass.
- `REVIEW`: repair complete but explicit mutation/merge approval remains.
- `BLOCKED`: a deterministic/human-only stop condition exists.
- `TIMEOUT`: monitoring budget exhausted.
