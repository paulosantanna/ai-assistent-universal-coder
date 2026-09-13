---
name: github-operations
description: Governed Git and GitHub operations with runtime-only authentication, immutable safety denials, branch/PR/workflow management and Work Bundle integration.
---

# GitHub Operations

## Identity

A skill of the single canonical `codenavi-agent`. It does not create another agent identity and does not expose secrets to model context.

## Mission

Provide one governed surface for local Git and remote GitHub operations used by AEOS skills/playbooks, including branches, commits, remotes, pull requests, workflow inspection/rerun, releases, bundle handoff and merge preparation.

## Authentication

Credentials are runtime-only. Configuration stores only a reference, for example:

```yaml
github:
  auth:
    type: environment
    token_env: GITHUB_PAT
```

Preferred sources: Git Credential Manager, `gh auth`, authorized secret provider, or environment reference. Never commit, print, log, cache, persist or send the PAT/token to reasoning, evidence, notebook or Token Manager.

A plaintext PAT in tracked YAML/config is a blocking secret-exposure finding. Remove the value from tracked config and require rotation/remediation according to repository policy; do not copy the value into reports or commits.

## Supported operation classes

### Read-only

- repository metadata, refs, diff/log/status;
- pull requests/issues/releases metadata;
- workflow/runs/jobs/checks and redacted logs;
- branch protection/rulesets when permissions allow;
- artifact metadata and rate-limit state.

### Governed mutation

- create/switch/rename branches;
- selective stage and atomic commit;
- fetch/pull/push authorized branches;
- create/update pull requests (Why/Porquê section required);
- rerun failed workflow runs/jobs;
- create draft releases and authorized releases;
- create/verify Git bundles;
- approved merge after latest-SHA revalidation and a verified Why/Porquê section.

High-risk mutation requires Policy/Permission/Judge/approval as defined by the calling playbook.

## Immutable denials

Always deny:

- repository deletion by API, CLI, script, workflow or delegation;
- reading/exporting existing secret values;
- PAT/token disclosure or scope escalation;
- branch-protection bypass;
- audit/evidence deletion;
- finalized evidence rewrite;
- force-push unless a future stricter policy explicitly introduces a separately approved exception; current default is deny.

Repository deletion response:

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

AEOS may state that repository deletion must be performed manually by the user in GitHub, but must not generate or execute a deletion command/API call.

## Pull request Why contract

Every open pull request MUST describe **why** the change exists, not only what changed. The Why/Porquê section is required so later worktrees, reviews and continuity notes keep adequate context.

Required body section (English `Why` or Portuguese `Porquê`/`Porque`):

```markdown
## Why
<motivation, problem, constraint or knowledge gap this change exists to solve>
```

Rules:

- `github.pull_request.create` and `github.pull_request.update` are blocked when the body lacks a Why/Porquê section, the section is empty, or it is a placeholder (`TBD`, `N/A`, `see title`, `see diff`).
- Why must explain motivation/context for the worktree. Restating the title or listing files is not sufficient.
- Merge readiness and merge execution inherit this gate. A green pipeline does not authorize merge when Why is missing.
- Do not invent a Why. If the operator cannot state why the change exists, stop and request that context.

## Operation planning

Every mutable operation records operation id, repository, branch/ref, risk, affected resources, preconditions, intended Git/API actions, rollback/compensation, policy decision, permission decision and approval requirement. The plan must not contain credentials or secret values.

## Command safety

Use structured argument arrays and repository-root validation. Do not construct shell command strings from untrusted input, do not use `shell=true`, and reject control operators/path traversal/protocol handlers outside policy.

## Integration

`devops-pipeline-engineering` depends on this skill for Git/GitHub mutation while retaining its own CI recovery logic. Work Bundle Mode depends on this skill for branch/commit/ref operations and transport verification.

## Completion

Return explicit operation result, evidence refs and rollback/compensation. Never report a mutation as complete when the remote state was not re-read and verified.
