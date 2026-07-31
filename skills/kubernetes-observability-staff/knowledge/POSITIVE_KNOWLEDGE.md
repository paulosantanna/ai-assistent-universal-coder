# POSITIVE_KNOWLEDGE.md

Validated positive knowledge for Kubernetes Observability Staff.

- Start from Kubernetes object state and events, then correlate with metrics and logs. Treat pod phase as a high-level summary only; inspect container states, conditions, reasons, messages, restart counts and probe behavior.
- Strong RCA starts with a bounded incident window, a signal matrix and a timeline that distinguishes first symptom, first user impact, first alert, first deployment/configuration change and recovery.
- A useful remediation proposal must be simple, scoped, testable, reversible and mapped to evidence.
