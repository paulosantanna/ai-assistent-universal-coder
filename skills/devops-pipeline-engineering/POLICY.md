# DevOps Pipeline Engineering Policy

## Risk model

- `read_only`: inspect repository, refs, workflows, runs, jobs, checks and redacted logs.
- `low`: generate plans, reports, bundles and local-only artifacts.
- `medium`: create branch, selective stage, commit, push to non-protected branch, create/update PR.
- `high`: workflow mutation, branch-protection change, release publication, merge execution.
- `destructive`: branch deletion, history rewrite, environment mutation.
- `permanently_denied`: repository deletion, secret-value read/export, audit-trail deletion, branch-protection bypass.

## Recursive recovery policy

Recovery may repeat only while all are true:

1. the latest SHA remains the active repair target;
2. the failure is in an authorized scope;
3. a root-cause hypothesis has evidence;
4. the proposed patch passes Chief/Staff self-review;
5. local focused verification passes or the failure is remote-only with documented evidence;
6. token/time/cycle budgets remain available;
7. progress detector does not report no-progress or oscillation;
8. no human-only gate is required.

## Required stop conditions

Return `BLOCKED` for:

- `RECOVERY_CYCLE_LIMIT_REACHED`
- `ROOT_CAUSE_RETRY_LIMIT_REACHED`
- `REPEATED_FAILURE_WITHOUT_PROGRESS`
- `RECOVERY_OSCILLATION_DETECTED`
- `TOKEN_BUDGET_EXCEEDED`
- `MONITOR_TIMEOUT`
- `SECRET_VALUE_REQUIRED`
- `PAT_SCOPE_INSUFFICIENT`
- `HUMAN_APPROVAL_REQUIRED`
- `BRANCH_PROTECTION_REQUIRES_HUMAN`
- `EXTERNAL_SERVICE_FAILURE`
- `GITHUB_PLATFORM_INCIDENT`
- `REPOSITORY_DELETION_MANUAL_ONLY`

## Merge policy

Default: `approval_required`.

A merge plan must record PR, base, expected head SHA, required checks, Judge status, evidence status, secret-scan status, protection/review status, merge strategy and rollback/compensation.

Merge execution must re-fetch the head SHA and required checks immediately before mutation. Head movement invalidates approval and requires revalidation.

## Secret policy

PAT/credentials remain runtime-only. YAML/config stores only a reference such as `env://GITHUB_PAT`. Never persist or echo the secret value. A plaintext token found in tracked configuration is a blocking incident requiring removal from history/rotation planning according to repository policy.

## Permanent repository deletion deny

`repository.delete` is denied before planning, approval, tool routing or API invocation. No approval or owner status can override it. AEOS may only tell the user that deletion must be performed manually in GitHub.
