<!-- Package: 00_skills/(security)/mantis-review; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# mantis-review

```yaml
skill:
  name: mantis-review
  slug: mantis-review
  version: 1.0.0
  description: Independently reviews findings and filters out false positives. Use when consolidated findings need validation against the actual source code. Don't use for reproducing crashes or patching code.
  category: SECURITY
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests Mantis defensive security review stage mantis-review or the mantis playbook routes to this stage
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
