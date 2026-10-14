<!-- Package: 00_skills/(cloud)/devops-pipeline-engineering; relative command/resource examples resolve from that package or workspace root. -->

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
11. Merge defaults to `approval_required` and is allowed only against the expected latest SHA after revalidation, and only when the open PR has a verified Why/Porquê section.
12. Secrets are runtime-only and never enter prompts, Token Manager context, logs, evidence, notebook, bundles or commits.
