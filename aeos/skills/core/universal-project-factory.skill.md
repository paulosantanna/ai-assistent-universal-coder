# Skill: universal-project-factory

## Mission

Plan and generate a sandbox-first project from zero to production for any requested architecture, language set and database set.

## Allowed Actions

- Read authorized requirements and evidence refs.
- Request `universal-project` MCP through Tool Router.
- Request language documentation MCPs for version-specific claims.
- Generate sandbox scaffold manifests and reports.
- Generate change manifests and rollback plans for every generated file.
- Route architecture decisions through `chromatic-mega-brain`.
- Route final readiness through Judge.

## Forbidden Actions

- Mutate the active workspace outside approved sandbox or patch workflow.
- Invent architecture, language, database or deployment decisions.
- Generate production secrets.
- Skip tests, CI, observability, rollback or token budget gates.
- Expand scope beyond the requested project without approval.

## Required Inputs

- project_name
- objective
- architecture
- languages
- databases
- deployment_target
- token_budget

## Output Schema

```json
{
  "status": "PASS|REVIEW|BLOCKED",
  "project_plan": {},
  "stack_matrix": {},
  "scaffold_manifest": {},
  "scaffold_package": {},
  "production_checklist": {},
  "sandbox_dir": "",
  "generated_files": [],
  "change_count": 0,
  "change_manifest": "",
  "rollback_plan": "",
  "rollback_summary": "",
  "required_playbooks": [],
  "evidence_refs": [],
  "blocking_conditions": []
}
```

## Workflow

1. Validate required inputs and token budget before any broad planning.
2. Use `chromatic-decision` for architecture or deployment tradeoffs.
3. Use `project.plan`, `project.stack_matrix`, `project.scaffold_manifest` and `project.production_checklist`.
4. Use `project.scaffold_package` to generate concrete sandbox-first files.
5. Select language documentation MCPs only for the requested languages.
6. Write generated files only under approved sandbox output.
7. Emit `change-manifest.json`, `rollback-plan.json` and `rollback-plan.md` for generated files.
8. Require tests, CI, security, observability, deployment and rollback artifacts.
9. Stop with `REVIEW` when a human architecture, language or database decision is missing.

## Quality Gates

- Every generated artifact maps to a requested requirement.
- Runtime versions and database choices are explicit.
- Concrete files are generated in sandbox before application.
- Tests, CI, observability, security and rollback are included.
- Every generated file is represented in the change manifest and rollback plan.
- Token budget is evaluated and respected.
- Subagents receive minimal task contracts only.

## Stop Conditions

- Required input missing.
- Token budget blocked.
- Unsupported language or database without user confirmation.
- Required documentation MCP unavailable for version-specific claims.
- Production readiness gate missing.
- Change manifest or rollback plan missing.
