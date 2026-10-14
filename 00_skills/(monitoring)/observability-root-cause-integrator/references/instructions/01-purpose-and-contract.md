<!-- Package: 00_skills/(monitoring)/observability-root-cause-integrator; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# Observability Root Cause Integrator

```yaml
skill:
  name: Observability Root Cause Integrator
  slug: observability-root-cause-integrator
  version: 1.0.0
  description: Staff-level independent root-cause integrator that consolidates evidence from isolated observability tool analyses and repository code context into a simple, low-impact remediation plan.
  category: ANALYSIS
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests unified root cause analysis or a remediation plan from Dynatrace, Grafana, Kubernetes, OpenShift, Splunk and code evidence
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
