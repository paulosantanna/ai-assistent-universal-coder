# Playbook: zero-to-production-project

## Objective

Generate a governed project plan and sandbox scaffold from zero to production for any requested architecture, language set and database set.

## Required Skills

- token-budget-governor
- chromatic-mega-brain
- universal-project-factory
- change-trace-auditor
- database-architecture-planner
- production-deployment-planner
- documentation
- security-audit
- test-generation

## Required MCPs

- universal-project
- complete-docs
- filesystem-readonly
- filesystem-write-sandbox
- test-runner-controlled
- package-local
- relevant language documentation MCPs

## Required LCPs

- global-rules
- zero-to-production
- token-economy
- documentation-standards
- security-governance

## Steps

1. Evaluate token budget for the requested provider and model class.
2. Capture requirements: project name, objective, architecture, languages, databases and deployment target.
3. If architecture is unclear or high-impact, run `chromatic-decision`.
4. Generate project plan, stack matrix, scaffold manifest, scaffold package and production checklist through `universal-project`.
5. Select only the documentation MCPs required by the chosen languages.
6. Plan database schema, migrations, backup and restore.
7. Generate sandbox scaffold files, change manifest, rollback plan and documentation package.
8. Run `change-trace-auditor` against generated files before any application step.
9. Generate tests, CI, security, observability, deployment and rollback plans.
10. Run security and package review gates.
11. Run Judge for production readiness.

## Blocking Conditions

- Missing required project decision.
- Token budget blocked.
- Subagent scope is broader than assigned task.
- Missing tests, CI, security, observability, deployment or rollback.
- Missing change manifest or rollback plan for generated files.
- Rollback coverage below 100 percent.
- Missing database migration plan when database exists.
- Production readiness Judge is not PASS.

## Outputs

- project plan
- stack matrix
- sandbox scaffold manifest
- sandbox scaffold package
- change manifest
- rollback trace report
- database plan
- deployment plan
- documentation package
- test strategy
- security report
- production readiness report
