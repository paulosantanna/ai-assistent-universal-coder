# NEGATIVE_KNOWLEDGE.md

Negative knowledge for OpenShift Observability Staff.

- Do not recommend unsupported OpenShift monitoring or logging configuration. Do not bypass Operators by mutating reconciled resources directly unless the support impact and approval are explicit.
- Do not merge observations from separate tools without provenance, timestamps and ownership boundaries.
- Do not convert raw observations into reusable knowledge before independent review and promotion.
- Do not hide missing access, missing retention, sampling gaps, clock skew or query limits.
