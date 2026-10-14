<!-- Package: 00_skills/(cloud)/devops-pipeline-engineering; relative command/resource examples resolve from that package or workspace root. -->

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
