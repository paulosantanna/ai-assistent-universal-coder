# Technical procedure
Updated: 2026-10-15
Entry point: ../SKILL.md.

## Retrieval decisions
Use lexical retrieval for exact identifiers and rare terms; dense retrieval for paraphrases. Preserve both rankings before reciprocal-rank fusion. Record embedding model/revision/dimension/distance and rebuild incompatible vector indexes on model changes. Apply ACLs before reranking and context packing.

## Parsing and version lifecycle
Keep source/document/chunk identifiers, acquisition hash, document version and extraction boundaries. Tables and code require headings/identifiers; image-only PDF requires explicit OCR. The package baseline uses character chunks; tokenize before context/training limits. An acquired source is not indexed, and a partially indexed document is not answer evidence.

## Grounding and measurement
Track retrieval recall separately from generation. Missing evidence must abstain. Citation-number validity is structural; evaluate support for each claim against the cited span. Prefer a frozen representative query set with gold evidence IDs, negative questions and old-version checks. Use nDCG/MRR for ranking and sampled human correctness for technical answers.

## Existing project adaptation
Reuse working parsers/stores/providers. Do not replace a pipeline simply to introduce GraphRAG or Laya. Compare hybrid, graph and Laya-assisted candidates on the same corpus and questions before adopting the additional step.
