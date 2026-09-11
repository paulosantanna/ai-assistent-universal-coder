# Local AGENT contract — github-operations

This local contract specializes the root `AGENT.md`. It does not create a second agent identity; all Git/GitHub work is owned by the canonical `codenavi-agent`.

## Mission lifecycle

Use `BRIEFING -> RECON -> PLAN -> EXECUTE -> VERIFY -> DEBRIEF` for every material mutation.

## Mandatory rules

- Resolve repository, base/head refs, remote, branch protection and authorization scope before mutation.
- Use runtime-only authentication references; never expose the credential value to reasoning, logs, evidence, notebook or bundles.
- Re-read remote state after mutation and verify the expected SHA/resource state.
- Prefer atomic commits and selective staging.
- Never use force-push by default.
- Never bypass branch protection or required reviews/checks.
- Never read/export existing GitHub secret values or widen PAT scopes automatically.
- Repository deletion is permanently denied and manual-only outside AEOS.
- A tool/API HTTP success is not proof that the intended Git/GitHub state was reached; verify state after action.

## High-risk gate

Merge, branch deletion, branch-protection mutation, release publication and workflow dispatch require explicit policy/approval for the current execution. Approval is bound to the expected repository/ref/SHA and becomes stale if those inputs move.

## Failure behavior

Fail closed on missing evidence, ambiguous repository/ref, insufficient permission, stale expected SHA, secret exposure, protection conflict or any permanently denied operation.
