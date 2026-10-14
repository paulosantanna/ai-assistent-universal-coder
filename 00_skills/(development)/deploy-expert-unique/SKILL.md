---
name: deploy-expert-unique
description: Apply the unique governed AWS deployment pipeline contract for AIHealthResearch, including branch promotion, Google OSV CVE, CodeQL SAST, Python security and deploy validators. Use when the user requests deploy expert unique or invokes deploy-expert-unique. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Deploy Expert Unique

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Use this skill only for the AIHealthResearch AWS deployment pipeline. It is intentionally project-specific and must not be generalized to unrelated repositories.

## Immutable pipeline contract

- Repository: `paulosantanna/AIHealthResearch`.
- Branch flow: feature branches merge to `develop`, `develop` promotes to `master`, and `master` promotes to `main`.
- `develop` validates only and must not mutate AWS.
- `master` deploys PRE through the GitHub Environment `pre`.
- `main` deploys production through the GitHub Environment `prod`.
- AWS deploy requires `AWS_DEPLOY_ENABLED=true` in the target environment.
- AWS auth must use GitHub OIDC and must not use static `AWS_ACCESS_KEY_ID` or `AWS_SECRET_ACCESS_KEY`.
- CloudFormation must deploy `infra/foundation.json` before `infra/workloads.json`.

## Required GitHub gates

- CVEs Google expert: `google/osv-scanner-action/osv-scanner-action@v2.6.0` with `--no-resolve` against the declared runtime manifest. Transitive dependency CVEs are governed by the lock-file `pip-audit` checks.
- SAST-expert: `github/codeql-action/init@v3` and `github/codeql-action/analyze@v3` for Python with `upload: false`, followed by `python scripts/validate_codeql_sarif.py codeql-results` so findings fail locally without depending on repository Code Scanning being enabled.
- Security-expert: `bandit -q -r src scripts`, `pip-audit -r requirements.lock`, and `pip-audit -r requirements-training.lock`.
- deploy-expert contract gate: `python scripts/validate_deployment_pipeline.py` and `python scripts/validate_security_gates.py`.

## Required AWS variables

The `pre` and `prod` GitHub Environments must define `AWS_DEPLOY_ENABLED`, `AWS_REGION`, `AWS_ROLE_TO_ASSUME`, `AWS_S3_PREFIX_LIST_ID`, `POSTGRES_ENGINE_VERSION`, `SEARCH_DOMAIN_NAME`, `APPLICATION_SECRET_ARN`, `CERTIFICATE_ARN`, `WORKER_SUBJECT`, `WORKER_TENANT`, `MODEL_DATA_URL`, `API_IMAGE`, `WORKER_IMAGE`, `MODEL_IMAGE`, and `MODEL_INSTANCE_TYPE`. `AWS_STACK_PREFIX` and `SCHEDULE_STATE` are optional. `SCHEDULE_STATE` must default to `DISABLED`.

## Review stance

Reject a deployment change when any gate is removed, bypassed, downgraded to warning-only, or made branch-ambiguous. Ask the failure-impact question before approval: if this fails here, which environment, stack, data class, scientific evidence path, model artifact, or training workflow is affected?

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
