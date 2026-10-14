# NEGATIVE_KNOWLEDGE.md

Negative knowledge for Grafana Observability Staff.

- Do not infer root cause from a single Grafana panel. Do not trust missing data as healthy behavior; first check instrumentation quality, labels, datasource freshness, scrape gaps, retention and query filters.
- Do not merge observations from separate tools without provenance, timestamps and ownership boundaries.
- Do not convert raw observations into reusable knowledge before independent review and promotion.
- Do not hide missing access, missing retention, sampling gaps, clock skew or query limits.
