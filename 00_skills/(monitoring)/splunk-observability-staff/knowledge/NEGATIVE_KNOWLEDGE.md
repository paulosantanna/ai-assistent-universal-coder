# NEGATIVE_KNOWLEDGE.md

Negative knowledge for Splunk Observability Staff.

- Do not treat a notable event title or high event count as root cause. Do not run broad all-time searches. Do not ignore search-time extraction gaps, index lag, clock skew, sourcetype drift or aggregation policy behavior.
- Do not merge observations from separate tools without provenance, timestamps and ownership boundaries.
- Do not convert raw observations into reusable knowledge before independent review and promotion.
- Do not hide missing access, missing retention, sampling gaps, clock skew or query limits.
