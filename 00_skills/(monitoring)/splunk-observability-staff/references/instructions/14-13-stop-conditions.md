<!-- Package: 00_skills/(monitoring)/splunk-observability-staff; relative command/resource examples resolve from that package or workspace root. -->

## 13. Stop conditions

Stop when:

- required Splunk evidence is unavailable or stale;
- the incident time window is unknown;
- permissions prevent required read-only analysis;
- telemetry retention, sampling or ingestion gaps invalidate the analysis;
- peer-agent communication is requested instead of evidence handoff;
- approval is required for a risky action;
- a critical blocker remains;
- the honest evaluator returns `BLOCKED`.
