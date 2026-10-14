<!-- Package: 00_skills/(security)/mantis-critic; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# mantis-critic

```yaml
skill:
  name: mantis-critic
  slug: mantis-critic
  version: 1.0.0
  description: Assesses the production viability of findings, filtering out debug-only features and assertion traps. Use when findings have been validated and you need to confirm they are triggerable in production release builds (with assertions disabled). Don't use for writing reproduction scripts or patches.
  category: SECURITY
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests Mantis defensive security review stage mantis-critic or the mantis playbook routes to this stage
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
