# GitHub Operations Policy

## Risk levels

- `read_only`: inspect repository, refs, workflows, checks and redacted logs.
- `low`: generate plans/reports/bundles without remote mutation.
- `medium`: branch creation, selective commit, push to authorized non-protected branch, PR create/update.
- `high`: workflow mutation, release publication, branch-protection update, merge.
- `destructive`: branch deletion/history-affecting operation; requires explicit approval and rollback/compensation.
- `permanently_denied`: repository deletion, secret-value extraction/export, PAT scope escalation, branch-protection bypass, finalized-evidence rewrite, audit deletion.

## Authentication policy

Tracked configuration may contain only a secret reference such as `env://GITHUB_PAT` or an approved credential-provider reference. A plaintext credential in tracked YAML/config blocks commit and requires remediation/rotation planning without reproducing the value.

## Mutation policy

Every mutable operation is bound to repository, ref/branch, expected SHA where applicable, risk class, policy decision, permission decision and rollback/compensation. Re-read remote state after mutation.

## Pull request Why policy

Every open PR body must include a Why/Porquê section that states the motivation for the change. This is required for worktree context and durable project knowledge. Create/update is denied when Why is missing, empty or a placeholder. Merge is denied on the same defect even if required checks are green.

## Merge policy

Default `approval_required`. Merge requires latest expected head SHA, successful required checks, branch protection/reviews satisfied, a verified Why/Porquê section, Judge PASS, Evidence Verify PASS and secret scan PASS. If head SHA changes, approval and CI evidence must be revalidated.

## Repository deletion

`repository.delete` is `DENY_PERMANENT`. Owner/admin status, PAT capabilities, policy overrides or approvals cannot enable it. AEOS may only direct the user to perform repository deletion manually in GitHub.
