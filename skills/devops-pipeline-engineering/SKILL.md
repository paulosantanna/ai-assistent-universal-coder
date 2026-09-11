---
name: devops-pipeline-engineering
description: Governed DevOps, Git and GitHub Actions lifecycle with recursive CI recovery, per-workflow guardians, merge readiness and bundle handoff.
---

# DevOps Pipeline Engineering

## Identity and inheritance

This is a **skill of the single canonical `codenavi-agent`**. It never creates or delegates to a second agent identity. Per-workflow and per-job specialization is represented by isolated **guardian lenses/work units**, each with its own bounded context, evidence and token budget.

The skill inherits root `AGENT.md`, `AGENTS.md`, `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`, Permission Engine, Policy Engine, Judge, Evidence, Token Manager and Work Bundle Mode. The stricter rule wins on conflict.

## Mission

Create, harden, operate and recover Git/GitHub CI/CD safely until every required GitHub Actions workflow for the latest head SHA is complete and successful, or a deterministic stop condition requires human action.

## Activation

Activate for:

- Git branch, commit, push, pull request and merge lifecycle;
- GitHub Actions creation, repair, rerun and monitoring;
- CI/CD failures and recursive recovery;
- branch-protection/readiness checks;
- release/bundle handoff after green CI;
- requests such as "corrija a esteira ate passar", "monitore todas as actions", "crie/mergeie o PR" or equivalent intent.

## Non-activation

Do not activate for unrelated code changes, production deployment not explicitly authorized, secret-value discovery or repository deletion.

## Core invariants

1. GitHub API HTTP 2xx means request success, **not pipeline success**.
2. Pipeline PASS requires every required run/job/check for the **latest head SHA** to be terminal and successful.
3. Previous-SHA results are invalidated after a corrective push.
4. Every relevant workflow run gets one `WorkflowGuardianLens`; every job/matrix child gets one bounded `JobGuardianWorkUnit`.
5. Guardians are execution contexts, **not agent identities**.
6. Equivalent failures are fingerprinted and grouped before repair; one root cause should produce one coordinated patch.
7. Recovery is recursive but bounded by cycle, progress, token and time limits.
8. Never hide failure with `continue-on-error`, arbitrary `skip/xfail`, removed tests, reduced coverage or disabled security gates.
9. Never force-push by default, bypass branch protection, invent secrets, read existing secret values or widen PAT scopes automatically.
10. Repository deletion is `DENY_PERMANENT` even if requested by the owner. It can only be performed manually outside AEOS.
11. Merge defaults to `approval_required` and is allowed only against the expected latest SHA after revalidation.
12. Secrets are runtime-only and never enter prompts, Token Manager context, logs, evidence, notebook, bundles or commits.

## Success contract

A run may report `PASS` only when:

```json
{
  "latest_sha_only": true,
  "required_workflows_completed": true,
  "required_workflows_success": true,
  "required_jobs_success": true,
  "required_checks_success": true,
  "pending_required_checks": 0,
  "judge": "PASS",
  "evidence_verify": "PASS",
  "secret_scan": "PASS"
}
```

`neutral` or `skipped` is acceptable only when the check is explicitly non-required by repository policy.

## Guardian lenses

The skill may instantiate these bounded lenses/work units under `codenavi-agent`:

- `workflow-guardian`: one per relevant workflow run;
- `job-guardian`: one per job/matrix child;
- `github-actions-architecture`: workflow YAML, expressions, permissions, matrix and reusable workflows;
- `python-ci`: pytest, packaging, lint, typing and Python compatibility;
- `java-maven-ci`: Maven/JUnit/Surefire/Failsafe/JaCoCo;
- `java-gradle-ci`: Gradle wrapper/tasks/tests/caches;
- `node-ci`: npm/pnpm/yarn/Bun, TypeScript and frontend builds;
- `docker-ci`: Dockerfile/buildx/compose/registry/container smoke;
- `infrastructure-ci`: Terraform/Kubernetes/Helm validation without unauthorized deploy;
- `security-ci`: secret scanning, permissions, OIDC, supply chain and artifact integrity;
- `dependency-recovery`: lockfiles, constraints and dependency conflicts;
- `test-recovery`: deterministic reproduction, fixture isolation and flaky-test diagnosis;
- `performance-ci`: timeout, resource and cache analysis;
- `release-engineering`: artifacts, tags, bundles, provenance and release readiness;
- `branch-protection`: required checks and protection validation without bypass;
- `pr-governance`: review/readiness/merge evidence;
- `rollback-recovery`: safe compensation plan;
- `token-economy`: compact evidence packets, cache and budget enforcement.

Each lens asks: **Would a Chief/Staff engineer of this specialization implement the fix this way, given root cause, architecture, security, maintainability, cost, observability, rollback and production impact?** Verdicts are `APPROVED`, `NEEDS_REWORK` or `REJECTED`.

## Recursive recovery lifecycle

`DISCOVER -> MONITOR -> CLASSIFY -> GROUP_ROOT_CAUSES -> REPRODUCE -> PLAN -> PATCH -> VERIFY_LOCAL -> JUDGE -> COMMIT -> AUTHORIZED_PUSH -> REDISCOVER`

Repeat only the recovery segment. Do not rerun unrelated setup work blindly.

Default limits:

```yaml
max_cycles: 10
max_cycles_per_root_cause: 3
max_total_commits: 20
max_commits_per_cycle: 3
max_same_fingerprint_repetitions: 2
poll_interval_seconds: 30
monitor_timeout_minutes: 180
discovery_quiet_period_seconds: 60
parallel_failure_analysis: true
parallel_limit: 8
serialize_overlapping_files: true
require_progress: true
stop_on_oscillation: true
```

Stop with `BLOCKED` on cycle exhaustion, repeated no-progress fingerprints, oscillation, missing secret value, insufficient PAT scope, external/GitHub outage, required human reviewer/environment approval, destructive migration, unauthorized deploy or any permanent deny.

## Git/GitHub authority

Allowed when policies/gates permit: inspect, branch, selective stage, commit, fetch, pull, push, PR create/update, workflow inspect/rerun, issue/release metadata, bundle create/verify, check/status inspection and approved merge.

High-risk operations require approval and revalidation. Force-push remains disabled by default.

### Permanent repository-deletion deny

Any repository deletion request resolves to:

```json
{
  "decision": "DENY_PERMANENT",
  "operation": "repository.delete",
  "reason_code": "REPOSITORY_DELETION_MANUAL_ONLY",
  "overridable": false,
  "approval_allowed": false,
  "delegation_allowed": false
}
```

User-facing message: `Repository deletion is permanently disabled in AEOS and must be performed manually by the user through GitHub.`

## Token economy

Never send whole successful logs or repository history to reasoning. Build compact evidence packets:

`redact secrets -> remove success noise -> extract failing step -> normalize stack -> fingerprint -> correlate diff -> relevant file excerpts -> evidence refs`.

Cache by SHA-256 and failure fingerprint. Guardians receive status metadata only unless a failure requires deeper analysis.

## Merge gate

Default mode: `approval_required`.

Merge prerequisites:

- expected head SHA unchanged;
- all required checks successful on that SHA;
- branch protection satisfied;
- no unresolved mandatory review/environment gate;
- secret scan PASS;
- Judge PASS;
- Evidence Verify PASS;
- rollback/compensation documented.

Never merge using stale CI evidence.

## Outputs

- workflow/run/job inventory;
- guardian state map;
- normalized failure records and fingerprints;
- root-cause groups;
- recovery-cycle plans/results;
- local verification results;
- commit/push evidence;
- final CI status for latest SHA;
- merge readiness decision;
- token-budget report;
- bundle manifest/verification when requested.

## Completion

Complete only as `PASS`, `BLOCKED`, `REVIEW` or `TIMEOUT`; never silently downgrade failures. A PASS is invalid while any required check for the latest SHA is pending or unsuccessful.
