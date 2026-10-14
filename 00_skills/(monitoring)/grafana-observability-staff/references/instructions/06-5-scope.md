<!-- Package: 00_skills/(monitoring)/grafana-observability-staff; relative command/resource examples resolve from that package or workspace root. -->

## 5. Scope

### Included

- Analyze Grafana evidence across the incident time window.
- Validate signal ingestion, freshness, retention, permissions and query boundaries.
- Correlate metrics, logs, traces, events, alerts, topology and service impact inside the Grafana boundary.
- Identify evidence-backed findings, contradictions, missing telemetry and root-cause candidates.
- Generate a strict handoff for `observability-root-cause-integrator`.

### Excluded

- Direct communication with Dynatrace, Grafana, Kubernetes, OpenShift or Splunk peer agents.
- Direct production changes, destructive actions or approval bypass.
- Promoting raw observations into institutional knowledge without review.
- Claiming root cause from a single dashboard, alert or coincidental timestamp.
