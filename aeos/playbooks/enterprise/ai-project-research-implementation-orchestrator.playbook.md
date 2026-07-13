# Enterprise Playbook: ai-project-research-implementation-orchestrator

## Objective

Coordinate the best AEOS MCPs to start research, architecture selection,
implementation planning, documentation, tests and release evidence for any AI
project request.

## Inputs

- target project path or new project name;
- objective;
- domain;
- architecture constraints;
- language and database choices;
- deployment target;
- risk level: `low`, `medium`, `high` or `medical`.

## Required Agents

- Root
- Planner
- Architect
- Domain Researcher
- Coder
- Tester
- Security
- DevOps
- Documenter
- Judge

## Required MCPs

- universal-project
- continuous-training
- complete-docs
- filesystem-readonly
- filesystem-write-sandbox
- git-readonly
- test-runner-controlled
- package-local
- medical-research, when risk level is `medical`
- docs-opentelemetry
- docs-grafana
- docs-dynatrace
- docs-observability-dashboards
- relevant language documentation MCPs

## Execution Flow

1. Classify risk and token budget before subagent delegation.
2. If project is new, call:
   - `universal-project.project.plan`;
   - `universal-project.project.stack_matrix`;
   - `universal-project.project.scaffold_manifest`;
   - `universal-project.project.production_checklist`.
3. If project exists, inspect repository through read-only MCPs.
4. For AI training or RAG decisions, call `continuous-training.best_practices` and
   `continuous-training.full_search`.
5. For medical or diabetes domain, call `medical-diabetes-research-to-implementation`
   as a required child playbook.
6. For evidence retrieval, call `evidence-rag-knowledge-base-bootstrap` as needed.
7. For runtime migration, call `language-upgrade-research-implementation` as needed.
8. For traces, metrics, logs and dashboards, call `observability-trace-metrics-logs`.
9. Generate documentation through `complete-docs`.
10. Generate sandbox implementation artifacts only, then run tests and package verification.
11. Run Judge with explicit PASS, BLOCKED or NEEDS HUMAN REVIEW.

## Blocking Conditions

- objective is missing;
- token budget is missing for LLM-heavy work;
- selected MCP does not match the domain;
- medical project bypasses medical-research source policy;
- implementation is not sandboxed;
- no tests, docs, rollback or evidence bundle exists;
- Judge decision is not PASS.

## Outputs

- `.aeos/reports/{execution_id}/orchestration-plan.md`
- `.aeos/evidence/{execution_id}/mcp-call-plan.json`
- `.aeos/tmp/{execution_id}/implementation-sandbox/`
- `.aeos/reports/{execution_id}/documentation-package.md`
- `.aeos/reports/{execution_id}/verification-summary.md`
- `.aeos/packages/{execution_id}/delivery-bundle.zip`
