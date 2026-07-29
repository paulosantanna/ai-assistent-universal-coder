# POSITIVE_KNOWLEDGE.md

Validated positive knowledge for Grafana Observability Staff.

- Use RED metrics to frame service health, then pivot through traces and logs using labels such as service namespace, deployment environment and job. Inspect query definitions behind panels before trusting dashboard visuals.
- Strong RCA starts with a bounded incident window, a signal matrix and a timeline that distinguishes first symptom, first user impact, first alert, first deployment/configuration change and recovery.
- A useful remediation proposal must be simple, scoped, testable, reversible and mapped to evidence.
