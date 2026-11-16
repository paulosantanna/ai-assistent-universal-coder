# Examples and realistic failures
Updated: 2026-10-15
Entry point: ../SKILL.md.

## implementar RAG sobre documentação técnica
Input: implementar RAG sobre documentação técnica.
Actions: Ingest authorized documents, retain source/version IDs, query lexical+vector baselines and return cited answers.
Observable output: Indexed corpus and report distinguishing retrieval quality from answer support.

## avaliar RAG com respostas sem fonte
Input: avaliar RAG com respostas sem fonte.
Actions: Freeze answer/evidence cases, reproduce missing citations, correct context identity and verify abstention.
Observable output: Evidence-backed before/after with unresolved entailment cases listed.

## RAG-expert para adicionar GraphRAG
Input: RAG-expert para adicionar GraphRAG.
Actions: Measure current retrieval, then compose ragraph-expert for relationships without duplicating general ingestion.
Observable output: Comparable hybrid/graph results with costs and sources.

## Negative boundary
Requests for unrelated graph visualization, standalone Laya training, production deployment do not activate this procedure; route to an applicable skill with observed prerequisites.

## Failure cases
Unknown source or missing permission -> stop dependent acquisition. Unavailable model/Neo4j -> report actual health. Invalid extraction/citations -> reject unsupported output. Dataset contamination -> rebuild disjoint partitions. Training OOM -> preserve experiment failure and base; do not silently promote. Missing human review -> retain pending state.
