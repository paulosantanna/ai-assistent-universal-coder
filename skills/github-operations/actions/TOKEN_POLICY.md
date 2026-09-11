# GitHub Actions Token Policy

Guardians are intentionally cheap contexts. They receive state metadata only until a failure requires diagnosis.

## Reduction pipeline

`raw log -> redact secrets -> remove successful-step noise -> extract failing step -> normalize stack/error -> fingerprint -> correlate with changed files -> compact evidence packet`.

## Allowed context

- workflow/run/job IDs and status;
- latest head SHA;
- normalized failure summary/fingerprint;
- relevant stack excerpt after redaction;
- changed-file summary and small relevant excerpts;
- evidence references;
- architecture summary cache key.

## Forbidden context

- PAT/token/Authorization/cookies;
- secret values;
- whole successful logs;
- complete Git history;
- unrelated files;
- binary artifacts/datasets/models.

## Cache

Reuse immutable analysis by head SHA, workflow attempt, file SHA-256 and failure fingerprint. A new head SHA invalidates dependent CI-state caches.

## Budgets

```yaml
global_recovery: 240000
per_cycle: 40000
per_root_cause: 14000
workflow_guardian: 3000
job_guardian: 1500
specialist_lens: 10000
judge: 10000
```

If the same failure fingerprint repeats without new evidence/progress, stop instead of repeatedly spending tokens.
