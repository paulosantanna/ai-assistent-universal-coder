<!-- Package: 00_skills/(security)/mantis-structural-index; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# mantis-structural-index

```yaml
skill:
  name: mantis-structural-index
  slug: mantis-structural-index
  version: 1.0.0
  description: Builds a content-addressed semantic-unit index from source code for structural context. Use when a pinned or live codebase is available and structural cross-reference data would improve research quality. Don't use for findings analysis, patching, or reporting.
  category: SECURITY
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests Mantis defensive security review stage mantis-structural-index or the mantis playbook routes to this stage
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
