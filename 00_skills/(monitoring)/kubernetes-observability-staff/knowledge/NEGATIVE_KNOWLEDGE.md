# NEGATIVE_KNOWLEDGE.md

Negative knowledge for Kubernetes Observability Staff.

- Do not diagnose from pod phase alone. Do not assume metrics-server provides complete observability; it exposes limited CPU and memory resource metrics mainly for autoscaling and top-style usage.
- Do not merge observations from separate tools without provenance, timestamps and ownership boundaries.
- Do not convert raw observations into reusable knowledge before independent review and promotion.
- Do not hide missing access, missing retention, sampling gaps, clock skew or query limits.
