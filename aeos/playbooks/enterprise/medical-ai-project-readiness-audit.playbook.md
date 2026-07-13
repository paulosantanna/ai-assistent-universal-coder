# Enterprise Playbook: medical-ai-project-readiness-audit

## Objective

Audit a medical AI project, especially diabetes-focused systems, for evidence
quality, architecture, RAG safety, training governance, observability, security
and production readiness.

## Inputs

- target project path;
- audit mode: `structural` or `deep`;
- medical domain scope;
- expected AI capabilities;
- deployment target;
- whether tests, security and dependency audits may run.

## Required Agents

- Root
- Repository Cartographer
- Medical Evidence Researcher
- Architecture Governor
- Security
- Tester
- Judge

## Required MCPs

- medical-research
- filesystem-readonly
- git-readonly
- test-runner-controlled
- package-local
- complete-docs
- docs-opentelemetry
- docs-grafana
- docs-dynatrace
- docs-observability-dashboards

## Execution Flow

1. Capture current branch, status and diff through `git-readonly`.
2. Run `medical-research.qualified_medical_sources` and confirm the source policy.
3. Run `medical-research.diabetes_ai_project_review_gate` when the project is diabetes-related.
4. Scan repository with `medical-research.repository_scan`.
5. Inventory architecture with `medical-research.repository_architecture_inventory`.
6. Run `medical-research.medical_ai_audit` with read-only mode.
7. Run focused gates:
   - `medical-research.rag_quality_gate`;
   - `medical-research.continuous_learning_quality_gate`;
   - `medical-research.owasp_ai_gate`;
   - `medical-research.training_pipeline_design`.
8. Use observability MCPs to verify trace, metric, log and dashboard readiness.
9. Generate a documentation and remediation package with `complete-docs`.
10. Package the report bundle through `package-local` when requested.

## Blocking Conditions

- repository cannot be scanned;
- audit runs with write privileges;
- medical source registry is missing;
- autonomous diagnosis or treatment behavior exists without a blocking control;
- RAG lacks citation, abstention or contradiction handling;
- no audit trail exists for generated medical claims;
- test, security or dependency gate fails without remediation;
- production readiness is claimed without observability and rollback evidence.

## Outputs

- `.aeos/reports/{execution_id}/medical-ai-readiness-audit.md`
- `.aeos/evidence/{execution_id}/repository-inventory.json`
- `.aeos/evidence/{execution_id}/medical-ai-audit.json`
- `.aeos/evidence/{execution_id}/observability-readiness.json`
- `.aeos/reports/{execution_id}/remediation-playbook.md`
- `.aeos/packages/{execution_id}/readiness-bundle.zip`
