# POSITIVE_KNOWLEDGE.md

Validated positive knowledge for OpenShift Observability Staff.

- Separate OpenShift platform monitoring from user workload monitoring. Confirm whether logging, event routing and user workload monitoring are enabled before treating missing telemetry as application behavior.
- Strong RCA starts with a bounded incident window, a signal matrix and a timeline that distinguishes first symptom, first user impact, first alert, first deployment/configuration change and recovery.
- A useful remediation proposal must be simple, scoped, testable, reversible and mapped to evidence.
