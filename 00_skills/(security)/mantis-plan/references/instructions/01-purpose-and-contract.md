<!-- Package: 00_skills/(security)/mantis-plan; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# mantis-plan

```yaml
skill:
  name: mantis-plan
  slug: mantis-plan
  version: 1.0.0
  description: Formulates a targeted defensive security reviewing plan based on the active threat model and historical learnings. Use when starting a security review campaign to map the codebase boundaries and generate a roadmap (workspace/plan.json). Don't use for executing code reviews, writing test scripts, or patching code.
  category: SECURITY
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests Mantis defensive security review stage mantis-plan or the mantis playbook routes to this stage
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
