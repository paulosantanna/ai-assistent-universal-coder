<!-- Package: 00_skills/(cloud)/devops-pipeline-engineering; relative command/resource examples resolve from that package or workspace root. -->

## Git/GitHub authority

Allowed when policies/gates permit: inspect, branch, selective stage, commit, fetch, pull, push, PR create/update (Why/Porquê required), workflow inspect/rerun, issue/release metadata, bundle create/verify, check/status inspection and approved merge.

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
