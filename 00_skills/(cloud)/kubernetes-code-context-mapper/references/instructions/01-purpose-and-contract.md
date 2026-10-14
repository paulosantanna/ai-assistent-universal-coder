<!-- Package: 00_skills/(cloud)/kubernetes-code-context-mapper; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# Kubernetes Code Context Mapper

```yaml
skill:
  name: Kubernetes Code Context Mapper
  slug: kubernetes-code-context-mapper
  version: 1.0.0
  description: Map Kubernetes pods, workloads, services, labels, metrics, logs and deployment metadata back to repository code, owners, tests and remediation boundaries.
  category: ANALYSIS
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests pods junto ao codigo, Kubernetes code correlation, workload ownership mapping, namespace-to-repository mapping or deployment-to-code traceability
    - a bug, incident or architecture task needs pod, workload, service or deployment metadata mapped to source code
  exclusions:
    - unrelated Kubernetes administration with no repository correlation need
    - production mutation without explicit approval
    - cluster access requests without read-only evidence boundaries
  inputs:
    - repository path or code map
    - Kubernetes evidence exports or read-only metadata
    - namespace, workload, pod, service or image identifier
  outputs:
    - workload_code_map.md
    - ownership_boundaries.md
    - telemetry_correlation.md
    - test_and_remediation_scope.md
    - evidence_index.md
  tools: []
  memory: true
  human_approval: true
  maintainer: AEOS
```
