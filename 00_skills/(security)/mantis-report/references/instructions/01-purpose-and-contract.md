<!-- Package: 00_skills/(security)/mantis-report; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# mantis-report

```yaml
skill:
  name: mantis-report
  slug: mantis-report
  version: 1.0.0
  description: Generates a human-readable security review packet compiled from confirmed findings and exploit chains. Use at the end of a review cycle to produce stakeholder-facing documentation. Don't use for auditing code or verifying patches directly.
  category: SECURITY
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests Mantis defensive security review stage mantis-report or the mantis playbook routes to this stage
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
