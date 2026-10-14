<!-- Package: 00_skills/(security)/mantis-pipeline-adapter; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# mantis-pipeline-adapter

```yaml
skill:
  name: mantis-pipeline-adapter
  slug: mantis-pipeline-adapter
  version: 1.0.0
  description: Interactively guides the design and implementation of custom deterministic orchestrator harnesses. Use when a user wants to build their own pipeline to wrap and run Mantis skills reliably. Don't use for executing the default pipeline directly.
  category: SECURITY
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests Mantis defensive security review stage mantis-pipeline-adapter or the mantis playbook routes to this stage
  exclusions:
    - unrelated requests`r`n- offensive security activity outside an authorized defensive review scope`r`n  inputs:
    - user request
  outputs:
    - validated result
  tools: []
  memory: true
  human_approval: true
  maintainer: AEOS
```
