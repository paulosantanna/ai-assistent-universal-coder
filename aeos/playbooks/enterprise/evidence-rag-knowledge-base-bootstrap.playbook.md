# Enterprise Playbook: evidence-rag-knowledge-base-bootstrap

## Objective

Create a governed evidence ingestion, RAG and knowledge-base implementation plan
for a project using medical, technical or language documentation sources.

## Inputs

- target project path;
- domain: `medical`, `engineering`, `language-docs` or `mixed`;
- source scope;
- retrieval strategy: `bm25`, `dense`, `hybrid` or `knowledge-graph`;
- storage target;
- languages and frameworks.

## Required Agents

- Root
- Evidence Researcher
- RAG Specialist
- Architect
- Coder
- Tester
- Judge

## Required MCPs

- medical-research, when domain includes medical evidence
- continuous-training, when domain includes AI engineering evidence
- complete-docs
- filesystem-readonly
- filesystem-write-sandbox
- test-runner-controlled
- relevant language documentation MCPs

## Execution Flow

1. Determine domain and allowed source classes.
2. For medical evidence, run:
   - `medical-research.qualified_medical_sources`;
   - `medical-research.medical_evidence_screening_policy`.
3. For AI engineering evidence, run:
   - `continuous-training.source_policy`;
   - `continuous-training.source_registry_list`;
   - `continuous-training.best_practices`.
4. For language implementation evidence, call only the matching language docs MCPs.
5. Inspect the target repository and identify current retrieval, storage and evaluation layers.
6. Design the evidence schema with fields for source, authority, date, evidence type,
   population or runtime, limitations, confidence and freshness.
7. Plan retrieval:
   - BM25 baseline;
   - dense retrieval only when embeddings are justified;
   - hybrid retrieval for production medical or high-risk technical use;
   - contradiction and abstention tests.
8. Generate sandbox artifacts:
   - source registry;
   - ingestion manifest;
   - schema files;
   - evaluator fixtures;
   - implementation checklist;
   - rollback plan.
9. Validate with `medical-research.rag_quality_gate` when medical RAG is in scope.
10. Generate docs and Mermaid diagrams through `complete-docs`.

## Blocking Conditions

- source policy is missing;
- medical evidence lacks human-review boundary;
- retrieval has no baseline evaluation;
- RAG answers cannot cite sources;
- no abstention behavior exists;
- no freshness, retraction or correction check exists for medical sources;
- generated implementation touches production files before sandbox review.

## Outputs

- `.aeos/tmp/{execution_id}/evidence-rag/source-registry.yaml`
- `.aeos/tmp/{execution_id}/evidence-rag/ingestion-manifest.json`
- `.aeos/tmp/{execution_id}/evidence-rag/evidence.schema.json`
- `.aeos/tmp/{execution_id}/evidence-rag/evaluator-fixtures/`
- `.aeos/reports/{execution_id}/rag-knowledge-base-plan.md`
- `.aeos/reports/{execution_id}/rag-validation-gates.md`
