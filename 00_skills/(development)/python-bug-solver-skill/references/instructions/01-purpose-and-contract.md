<!-- Package: 00_skills/(development)/python-bug-solver-skill; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# Python Bug Solver Skill

```yaml
skill:
  name: Python Bug Solver Skill
  slug: python-bug
  version: 1.0.0
  description: Create a Python Bug Solver skill that analyzes stack traces, searches for root causes, generates fixes, validates them and stores lessons learned
  category: REPAIR
  architecture_level: 3
  risk_level: CRITICAL
  activation:
    - the user requests create a Python Bug Solver skill that analyzes stack traces, searches for root causes, generates fixes, validates them and stores lessons learned
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
