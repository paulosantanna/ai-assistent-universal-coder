# Local AGENT contract — devops-pipeline-engineering

This file does **not** define a new agent identity. It specializes the root `AGENT.md` for this skill and inherits the single canonical `codenavi-agent` model.

## Local execution contract

- Follow `BRIEFING -> RECON -> PLAN -> EXECUTE -> VERIFY -> DEBRIEF`.
- Read repository-native CI/CD, branch protection, workflow, package manager and test conventions before mutation.
- Treat every workflow/job guardian as a bounded work unit/lens, never a subagent identity.
- Establish the failing SHA, run ID, job ID, step and normalized failure fingerprint before patching.
- Reproduce locally when technically feasible before changing code or workflow configuration.
- Fix root cause, not the symptom.
- Prefer the smallest repair that preserves existing quality gates.
- Every corrective push invalidates prior-SHA CI evidence.
- Re-discover all relevant workflow runs after each push.
- Never expose PATs, tokens, cookies, secret values or Authorization headers.
- Never widen PAT scopes automatically.
- Never bypass branch protection.
- Never auto-delete repositories; repository deletion is permanent deny.
- Never hide failure by disabling checks, deleting tests, weakening assertions, reducing coverage, arbitrary `continue-on-error`, or unjustified `skip/xfail`.

## Chief/Staff self-review

For each root-cause group, answer:

> Would a Chief/Staff engineer responsible for this domain implement this fix this way, considering root cause, architecture, security, maintainability, cost, observability, rollback and production impact?

Valid verdicts:

- `APPROVED`
- `NEEDS_REWORK`
- `REJECTED`

`REJECTED` blocks mutation. `NEEDS_REWORK` requires a revised plan before mutation.

## Progress requirement

A recovery cycle may continue only when there is measurable progress: fewer active failure fingerprints/jobs, a resolved root cause, a newly passing required check, or a workflow advancing because the previous blocker was removed.

A new commit alone is not progress.

## Merge requirement

Merge is `approval_required` by default and is permitted only after immediate revalidation of the expected latest head SHA and all mandatory repository gates.
