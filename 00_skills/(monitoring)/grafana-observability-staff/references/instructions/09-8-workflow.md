<!-- Package: 00_skills/(monitoring)/grafana-observability-staff; relative command/resource examples resolve from that package or workspace root. -->

## 8. Workflow

1. Declare objective, target scope, time window, permissions, assumptions and explicit non-goals.
2. Validate prerequisites: access level, time range, retention, clock skew, sampling, query limits, RBAC and redaction rules.
3. Spawn isolated child analyses inside this agent boundary only: dashboard-query-child, prometheus-promql-child, loki-logql-child, tempo-traceql-child, alerting-rule-child, instrumentation-quality-child.
4. Require each child analysis to return facts, exact evidence refs, negative findings, uncertainty, query boundaries and open risks.
5. Build a signal matrix: metrics, logs, traces, events, topology, alerts, deployments, saturation, errors, latency, traffic and resource pressure.
6. Build a timeline: first bad signal, first user impact, first alert, first deployment/config change, first recovery signal and unresolved gaps.
7. Challenge every root-cause candidate against counter-evidence and alternative explanations.
8. Separate facts from inference. Mark missing evidence as `UNVERIFIED` or `BLOCKED`.
9. Produce the handoff to `observability-root-cause-integrator`; do not communicate with peer tool agents.
10. Apply `evaluation/HONEST_EVALUATOR.md` before reporting completion.
