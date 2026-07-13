# Enterprise Playbook: medical-diabetes-research-to-implementation

## Objective

Start a governed diabetes research and implementation workflow for an AI project,
from source discovery to sandbox implementation plan, without producing clinical
diagnosis, treatment, triage, dosing or cure claims.

## Inputs

- target project path;
- research objective;
- diabetes subtype or population scope;
- comorbidities of interest;
- implementation target: `knowledge-base`, `rag`, `audit`, `evaluation`, `ui`, `api` or `pipeline`;
- languages and frameworks already used by the project;
- required deployment target.

## Required Agents

- Root
- Medical Evidence Researcher
- Architect
- Coder
- Tester
- Security
- Judge

## Required MCPs

- medical-research
- continuous-training
- complete-docs
- filesystem-readonly
- filesystem-write-sandbox
- test-runner-controlled
- relevant language documentation MCPs

## Execution Flow

1. Run `medical-research.qualified_medical_sources` and `medical-research.medical_evidence_screening_policy`.
2. Run `medical-research.diabetes_staff_expertise_map` to load the governed domain map.
3. Build disease and method queries through:
   - `medical-research.build_disease_research_query`;
   - `medical-research.build_research_method_queries`.
4. Search governed literature and trials:
   - `medical-research.pubmed_research`;
   - `medical-research.europe_pmc_research`;
   - `medical-research.clinical_trials_research`.
5. Use `continuous-training.full_search` only for AI engineering techniques,
   implementation patterns, evaluation harnesses and training infrastructure.
6. Inspect the target repository with:
   - `medical-research.repository_scan`;
   - `medical-research.repository_architecture_inventory`.
7. Select only the language documentation MCPs matching the detected stack.
8. Produce a sandbox implementation package containing:
   - evidence matrix;
   - source provenance table;
   - knowledge schema or RAG ingestion plan;
   - implementation patch plan;
   - tests and safety gates;
   - rollback plan.
9. Generate documentation with `complete-docs.docs.architecture_package`, including
   Mermaid diagrams for evidence flow, RAG flow, validation gates and human review.
10. Run project tests through `test-runner-controlled` and run `medical-research.expert_validation_10_0`.

## Blocking Conditions

- medical claim without governed source provenance;
- PubMed or Europe PMC evidence is absent for core claims;
- implementation changes patient-facing behavior without human review;
- generated output implies diagnosis, treatment, triage, dosing or cure;
- safety, privacy, audit or rollback gates are missing;
- tests are unavailable and no manual verification plan is produced;
- Judge does not pass.

## Outputs

- `.aeos/reports/{execution_id}/diabetes-research-brief.md`
- `.aeos/evidence/{execution_id}/medical-source-matrix.json`
- `.aeos/evidence/{execution_id}/implementation-plan.json`
- `.aeos/tmp/{execution_id}/sandbox-implementation/`
- `.aeos/reports/{execution_id}/architecture-package.md`
- `.aeos/reports/{execution_id}/judge-decision.md`

## Safety Boundary

This playbook is research-only and project-engineering-only. It may evaluate and
improve software architecture, evidence retrieval, governance and implementation
quality. It must not act as a clinician or make patient-specific medical decisions.
