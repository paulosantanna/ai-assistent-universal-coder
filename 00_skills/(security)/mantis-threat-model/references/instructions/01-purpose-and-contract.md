<!-- Package: 00_skills/(security)/mantis-threat-model; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# mantis-threat-model

```yaml
skill:
  name: mantis-threat-model
  slug: mantis-threat-model
  version: 1.0.0
  description: Synthesizes trust boundaries, attack surfaces, and attacker profiles into a living threat model. Use as Stage B of the Knowledge Base generation process, reading architecture and entity definitions from the KB. Don't use for analyzing source code or extracting raw learnings from JSONL files.
  category: SECURITY
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests Mantis defensive security review stage mantis-threat-model or the mantis playbook routes to this stage
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
