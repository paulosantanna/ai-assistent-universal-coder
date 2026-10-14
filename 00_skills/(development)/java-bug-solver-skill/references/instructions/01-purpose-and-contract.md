<!-- Package: 00_skills/(development)/java-bug-solver-skill; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# Java Bug Solver Skill

```yaml
skill:
  name: Java Bug Solver Skill
  slug: java-bug-solver-skill
  version: 1.0.0
  description: Create a Java Bug Solver skill that analyzes stack traces, searches for root causes, generates fixes, validates them and stores lessons learned
  category: REPAIR
  architecture_level: 3
  risk_level: MEDIUM
  activation:
    - the user requests create a Java Bug Solver skill that analyzes stack traces, searches for root causes, generates fixes, validates them and stores lessons learned
  exclusions:
    - unrelated requests
  inputs:
    - user request
  outputs:
    - validated result
  tools: []
  memory: true
  human_approval: false
  maintainer: AEOS
```
