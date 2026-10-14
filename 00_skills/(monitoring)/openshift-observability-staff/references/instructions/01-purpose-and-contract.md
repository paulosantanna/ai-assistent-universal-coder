<!-- Package: 00_skills/(monitoring)/openshift-observability-staff; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# OpenShift Observability Staff

```yaml
skill:
  name: OpenShift Observability Staff
  slug: openshift-observability-staff
  version: 1.0.0
  description: Deep Staff-level OpenShift observability analysis for platform monitoring, user workload monitoring, alerts, logging, operators, routes, builds, cluster health and supported configuration boundaries.
  category: ANALYSIS
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests deep OpenShift observability, monitoring, logging, operator, alert, route or cluster troubleshooting analysis
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
