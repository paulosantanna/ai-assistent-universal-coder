<!-- Package: 00_skills/(monitoring)/grafana-observability-staff; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# Grafana Observability Staff

```yaml
skill:
  name: Grafana Observability Staff
  slug: grafana-observability-staff
  version: 1.0.0
  description: Deep Staff-level Grafana observability analysis for dashboards, Prometheus metrics, Loki logs, Tempo traces, alerts, exemplars, service maps, SLOs and instrumentation quality.
  category: ANALYSIS
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests deep Grafana, Prometheus, Loki, Tempo, alerting, dashboard or service observability analysis
    - the analayze-metricas playbook assigns this isolated agent to produce evidence for root-cause analysis
  exclusions:
    - unrelated requests
    - requests to mutate production systems without explicit human approval
    - requests to accept observations without evidence
  inputs:
    - user objective
    - service or cluster identifier
    - incident time window with timezone
    - read-only telemetry access or exported evidence
    - repository path or code map when code correlation is required
  outputs:
    - tool_analysis_report.json
    - evidence-index.md
    - knowledge-candidates.md
    - handoff-to-root-cause-integrator.json
  tools: []
  memory: true
  human_approval: true
  maintainer: AEOS
```
