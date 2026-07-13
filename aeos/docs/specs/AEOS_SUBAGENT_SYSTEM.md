# AEOS Subagent System

## Purpose

Subagents perform narrow specialized work under a parent agent, without independent authority expansion.

## Subagent Types

```text
java-analyzer
spring-analyzer
python-rag-analyzer
test-gap-analyzer
dependency-risk-analyzer
security-secret-detector
docker-env-analyzer
docs-adr-writer
patch-risk-reviewer
rollback-reviewer
```

## Subagent Contract

```yaml
subagent:
  id:
  parent_agent:
  mission:
  max_scope:
  allowed_skills:
  forbidden_actions:
  required_context:
  required_evidence:
  timeout:
  output_schema:
```

## Rules

- Subagents cannot directly access MCPs.
- Subagents cannot request secrets.
- Subagents cannot approve actions.
- Subagents cannot mutate project files.
- Subagents cannot change architecture decisions.
- Subagents output analysis, recommendations, or proposed artifacts only.

## Output Schema

```json
{
  "subagent_id": "...",
  "task_id": "...",
  "status": "completed|blocked|failed",
  "facts": [],
  "assumptions": [],
  "risks": [],
  "recommendations": [],
  "evidence_refs": [],
  "blocking_conditions": []
}
```
