<!-- Package: 00_skills/(security)/mantis-researcher; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# mantis-researcher

```yaml
skill:
  name: mantis-researcher
  slug: mantis-researcher
  version: 1.0.0
  description: Audits production source code files based on the strategy in workspace/plan.json. Use when a review plan exists and you need to perform static analysis and deep-dive reviews of targeted files. Don't use for planning, deduplicating, or writing patches.
  category: SECURITY
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests Mantis defensive security review stage mantis-researcher or the mantis playbook routes to this stage
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
