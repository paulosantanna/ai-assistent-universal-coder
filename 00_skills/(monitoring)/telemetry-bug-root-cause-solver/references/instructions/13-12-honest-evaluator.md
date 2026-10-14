<!-- Package: 00_skills/(monitoring)/telemetry-bug-root-cause-solver; relative command/resource examples resolve from that package or workspace root. -->

## 12. Honest evaluator

Before completion, apply `evaluation/HONEST_EVALUATOR.md`.

The evaluator must reject:

- root-cause claims based on a single dashboard or log line;
- fixes with no failing reproduction or deterministic equivalent when reproduction is possible;
- skipped tests without residual risk disclosure;
- telemetry excerpts that omit query, time window or timezone;
- learning records that contain raw sensitive output.
