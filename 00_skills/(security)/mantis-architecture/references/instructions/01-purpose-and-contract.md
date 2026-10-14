<!-- Package: 00_skills/(security)/mantis-architecture; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# mantis-architecture

```yaml
skill:
  name: mantis-architecture
  slug: mantis-architecture
  version: 1.0.0
  description: Synthesizes raw learnings and codebase analysis into an interlinked Markdown Knowledge Base (KB). Use at the beginning of a loop to build or update architecture.md, entities, and vulnerabilities. Don't use for generating threat models or formulating execution plans.
  category: SECURITY
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests Mantis defensive security review stage mantis-architecture or the mantis playbook routes to this stage
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
