<!-- Package: 00_skills/(security)/mantis-meta-agent; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# mantis-meta-agent

```yaml
skill:
  name: mantis-meta-agent
  slug: mantis-meta-agent
  version: 1.0.0
  description: Acts as the persistent supervisor, launching and monitoring the automated review campaign. Use when running a long-running, continuous security review campaign that needs autonomous coordination. Don't use for executing individual review stages directly.
  category: SECURITY
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests Mantis defensive security review stage mantis-meta-agent or the mantis playbook routes to this stage
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
