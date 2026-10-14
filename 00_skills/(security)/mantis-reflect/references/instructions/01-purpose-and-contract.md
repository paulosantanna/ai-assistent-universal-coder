<!-- Package: 00_skills/(security)/mantis-reflect; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# mantis-reflect

```yaml
skill:
  name: mantis-reflect
  slug: mantis-reflect
  version: 1.0.0
  description: Extracts learnings from execution trajectories at the end of a Mantis loop. Use to parse agent conversations, extract successes, failures, and false assumptions, and append them to workspace/learnings.jsonl. Don't use for analyzing source code or writing patches.
  category: SECURITY
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests Mantis defensive security review stage mantis-reflect or the mantis playbook routes to this stage
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
