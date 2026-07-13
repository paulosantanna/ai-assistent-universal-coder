# Skill: production-deployment-planner

## Mission

Plan production packaging, CI/CD, deployment, observability, rollback and operational readiness for any architecture.

## Allowed Actions

- Read authorized build, deployment and evidence refs.
- Generate deployment plans and sandbox artifacts.
- Generate CI/CD and rollback checklists.
- Route final deployment readiness through Judge.

## Forbidden Actions

- Deploy automatically.
- Generate or expose secrets.
- Skip rollback.
- Skip observability.
- Treat local success as production readiness.

## Required Inputs

- architecture
- languages
- databases
- deployment_target
- ci_provider
- token_budget

## Output Schema

```json
{
  "status": "PASS|REVIEW|BLOCKED",
  "deployment_plan": {},
  "ci_cd_plan": {},
  "observability_plan": {},
  "rollback_plan": {},
  "readiness_gates": [],
  "blocking_conditions": []
}
```

## Quality Gates

- Build artifact is explicit for every runtime.
- CI/CD includes test and security gates.
- Deployment target and rollback are explicit.
- Observability includes logs, metrics and traces when applicable.
- Token budget is respected.

## Stop Conditions

- Deployment target missing.
- CI provider missing or explicitly out of scope.
- Rollback missing.
- Secret handling undefined.
