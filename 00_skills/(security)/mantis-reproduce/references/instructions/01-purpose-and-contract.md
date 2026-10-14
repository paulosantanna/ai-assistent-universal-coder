<!-- Package: 00_skills/(security)/mantis-reproduce; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# mantis-reproduce

```yaml
skill:
  name: mantis-reproduce
  slug: mantis-reproduce
  version: 1.0.0
  description: Generates and runs crash reproducers to verify security flaws. Use when viable findings exist and you need to write and execute a script or payload to verify the crash. Don't use for code auditing or patching.
  category: SECURITY
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests Mantis defensive security review stage mantis-reproduce or the mantis playbook routes to this stage
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
