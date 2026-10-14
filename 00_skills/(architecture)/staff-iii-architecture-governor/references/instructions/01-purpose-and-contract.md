<!-- Package: 00_skills/(architecture)/staff-iii-architecture-governor; relative command/resource examples resolve from that package or workspace root. -->

# SKILL.md
# staff-iii-architecture-governor

```yaml
skill:
  name: staff-iii-architecture-governor
  slug: staff-iii-architecture-governor
  version: 1.0.0
  description: Architect Staff III super skill for planning and selecting technologies, languages, architecture, CI/CD, GitHub Actions, Kubernetes, Docker, cybersecurity and database strategy through subagents and an extremely honest evaluator before project creation or architecture changes.
  category: ORCHESTRATION
  architecture_level: 3
  risk_level: HIGH
  activation:
    - the user requests staff architecture, Architect Staff III planning, technology selection, project architecture, CI/CD, GitHub Actions, Kubernetes, Docker, cybersecurity, database choice, production architecture, or architecture change planning
    - a project must be started without a user-specified language or technology stack
    - an existing project architecture must be evaluated or changed
  exclusions:
    - pure implementation without architecture plan
    - business-rule decisions that require product-owner or user authority
    - production deployment without explicit approval
  inputs:
    - user objective
    - repository path or greenfield project brief
    - known business rules and constraints
    - optional language, technology, database, cloud or compliance constraints
  outputs:
    - architecture_decision_record.md
    - technology_selection_matrix.md
    - database_decision.md
    - ci_cd_plan.md
    - github_actions_plan.md
    - kubernetes_docker_plan.md
    - cybersecurity_plan.md
    - honest_architecture_verdict.md
  tools: []
  memory: true
  human_approval: true
  maintainer: AEOS
```
