# Audit Log Retention Policy

## Defaults

```text
execution evidence: 180 days
approval records: 365 days
security reports: 365 days
observability logs: 90 days
packages: project-defined
```

## Rules

- Do not store secrets.
- Redact sensitive values.
- Preserve approval records.
- Preserve Judge reports.
- Preserve hash manifests.
