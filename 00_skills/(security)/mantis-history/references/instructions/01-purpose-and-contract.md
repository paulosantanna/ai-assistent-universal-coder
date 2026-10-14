<!-- Package: 00_skills/(security)/mantis-history; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# mantis-history

```yaml
skill:
  name: mantis-history
  slug: mantis-history
  version: 1.0.0
  description: Analyzes the repository's version control system (VCS) history to extract past vulnerabilities, security fixes, and vulnerability patterns. Use as an initial pre-processing step to build a historical vulnerabilities database (workspace/historical_learnings.jsonl) that informs subsequent stages about past issues and fixes. Don't use for code reviews, writing test scripts, or patching code.
  category: SECURITY
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests Mantis defensive security review stage mantis-history or the mantis playbook routes to this stage
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
