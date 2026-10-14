<!-- Package: 00_skills/(security)/mantis-chain; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# mantis-chain

```yaml
skill:
  name: mantis-chain
  slug: mantis-chain
  version: 1.0.0
  description: Analyzes individual security findings to identify and construct complex exploit chains. Use after validation stages to see if multiple low-severity bugs can be combined into a higher impact vulnerability. Don't use for initial codebase auditing or writing patch code.
  category: SECURITY
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests Mantis defensive security review stage mantis-chain or the mantis playbook routes to this stage
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
