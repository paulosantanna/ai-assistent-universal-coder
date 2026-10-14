<!-- Package: 00_skills/(security)/mantis-summarize; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# mantis-summarize

```yaml
skill:
  name: mantis-summarize
  slug: mantis-summarize
  version: 1.0.0
  description: Pre-processes the repository by generating security-focused summaries (mantis-summary.md) for each directory to make planning and research more efficient. Use when starting a review campaign to map the codebase before threat modeling and planning. Don't use for executing code reviews, writing test scripts, or patching code.
  category: SECURITY
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests Mantis defensive security review stage mantis-summarize or the mantis playbook routes to this stage
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
