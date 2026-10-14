<!-- Package: 00_skills/(creation)/skill-factory; relative command/resource examples resolve from that package or workspace root. -->

## 4. Intent classification

Classify the requested skill before generating it.

Allowed categories:

- `EXECUTION`
- `ANALYSIS`
- `RESEARCH`
- `GENERATION`
- `VALIDATION`
- `AUDIT`
- `ORCHESTRATION`
- `REPAIR`
- `MIGRATION`
- `DOCUMENTATION`
- `SECURITY`
- `TESTING`
- `DATA`
- `AI_ML`
- `CLINICAL`
- `GOVERNANCE`
- `HYBRID`

Determine:

```yaml
skill_intent:
  user_goal:
  primary_category:
  secondary_categories:
  expected_inputs:
  expected_outputs:
  target_repository_scope:
  risk_level:
  reusable_frequency:
  external_tools_required:
  memory_required:
  subagents_required:
  human_approval_required:
```

---
