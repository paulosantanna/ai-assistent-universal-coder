# Examples and realistic failures
Updated: 2026-10-15
Entry point: ../SKILL.md.

## Laya-expert para roteamento técnico
Input: Laya-expert para roteamento técnico.
Actions: Define lexical/hybrid/graph criteria, measure base predictions and add a low-confidence deterministic fallback.
Observable output: Typed routes with probabilities, checkpoint identity and no execution permissions.

## decisões Laya para reranking
Input: decisões Laya para reranking.
Actions: Score query/candidate pairs; compare nDCG and latency with unchanged hybrid order.
Observable output: Candidate relevance results and explicit uncertainty.

## fine-tuning Laya para RAG
Input: fine-tuning Laya para RAG.
Actions: Validate domain JSONL, train RLCD, calibrate, reload and evaluate base/candidate.
Observable output: Compatible checkpoint, metrics and pending human-review status.

## Negative boundary
Requests for open-ended text generation, GraphRAG indexing, production deployment do not activate this procedure; route to an applicable skill with observed prerequisites.

## Failure cases
Unknown source or missing permission -> stop dependent acquisition. Unavailable model/Neo4j -> report actual health. Invalid extraction/citations -> reject unsupported output. Dataset contamination -> rebuild disjoint partitions. Training OOM -> preserve experiment failure and base; do not silently promote. Missing human review -> retain pending state.
