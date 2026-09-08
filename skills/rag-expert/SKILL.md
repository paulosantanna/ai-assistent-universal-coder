# RAG Expert
Governance: CodENavi v1

## Mission
Implement or repair Retrieval-Augmented Generation systems with measurable grounding quality.

## Build path
Source authority/provenance → parsing → normalization/dedup → chunk strategy → metadata/ACLs → lexical + vector indexes → query rewrite when justified → retrieval → fusion → rerank → context packing → grounded generation → citations → evals/monitoring.

## Metrics
Recall@k, precision@k, MRR/nDCG where appropriate, answer correctness, faithfulness/groundedness, citation validity, latency and cost.

Use BM25 + embeddings as a strong hybrid baseline when corpus/query characteristics justify both lexical exactness and semantic recall. Prevent cross-tenant/ACL leakage before quality optimization.