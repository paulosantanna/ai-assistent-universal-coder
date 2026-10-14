<!-- Package: 00_skills/(monitoring)/splunk-observability-staff; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# Splunk Observability Staff

```yaml
skill:
  name: Splunk Observability Staff
  slug: splunk-observability-staff
  version: 1.0.0
  description: Deep Staff-level Splunk observability analysis for Splunk Enterprise, ITSI, Observability Cloud, searches, metrics, logs, traces, notable events, episodes and service-impact evidence.
  category: ANALYSIS
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests deep Splunk, ITSI, Observability Cloud, SPL, episode, notable event, metric, log or trace analysis
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
