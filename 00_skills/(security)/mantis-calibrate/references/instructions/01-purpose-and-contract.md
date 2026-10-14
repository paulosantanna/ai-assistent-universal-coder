<!-- Package: 00_skills/(security)/mantis-calibrate; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# mantis-calibrate

```yaml
skill:
  name: mantis-calibrate
  slug: mantis-calibrate
  version: 1.0.0
  description: Calculates the final risk score based on empirical evidence and architectural impact. Use when findings have been fully processed by previous stages and you need to append final risk scores to the finding files. Don't use for discovering new vulnerabilities or writing patches.
  category: SECURITY
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests Mantis defensive security review stage mantis-calibrate or the mantis playbook routes to this stage
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
