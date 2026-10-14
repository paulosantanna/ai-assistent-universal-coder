<!-- Package: 00_skills/(security)/mantis-patch; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# mantis-patch

```yaml
skill:
  name: mantis-patch
  slug: mantis-patch
  version: 1.0.0
  description: Generates minimal security fixes using transactional isolation (shadow directories or file backups), applies patches, and verifies them. Use when security findings are successfully reproduced and need patches applied and verified. Don't use for initial vulnerability research or reproduction payload generation.
  category: SECURITY
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests Mantis defensive security review stage mantis-patch or the mantis playbook routes to this stage
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
