# POSITIVE_KNOWLEDGE.md

Validated positive knowledge for Dynatrace Observability Staff.

- Use Dynatrace problems as hypotheses, not conclusions; verify Davis root-cause and impact analysis against entity topology, transaction/code-level context, Davis events, logs, metrics and traces. Treat Kubernetes/OpenShift events as first-class RCA evidence only when event monitoring is enabled and event timing aligns with affected entities.
- Strong RCA starts with a bounded incident window, a signal matrix and a timeline that distinguishes first symptom, first user impact, first alert, first deployment/configuration change and recovery.
- A useful remediation proposal must be simple, scoped, testable, reversible and mapped to evidence.
