# AEOS Workbench Profiles

Profiles define operating modes.

## Profiles

```text
java-enterprise
python-ai-rag
fullstack-docker
devops-platform
security-audit
documentation-factory
incident-response
legacy-modernization
ai-research
clinical-ai-governance
```

## Profile Contract

```yaml
profile:
  id:
  description:
  default_lcps:
  default_playbooks:
  default_skills:
  allowed_mcps:
  forbidden_actions:
  required_judge_gates:
  output_templates:
```

## Example

```yaml
profile:
  id: java-enterprise
  default_lcps:
    - global-rules
    - security-governance
    - java-backend
  default_playbooks:
    - project-analysis
    - dependency-analysis
    - test-recovery
    - code-change-proposal
  forbidden_actions:
    - auto_merge
    - production_deploy
    - secret_read
```
