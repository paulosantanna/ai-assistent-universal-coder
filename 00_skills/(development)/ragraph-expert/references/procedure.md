# Technical procedure
Updated: 2026-10-15
Entry point: ../SKILL.md.

## Engine selection
Microsoft GraphRAG extracts entity relationships and community reports for corpus-wide questions. LightRAG combines graph and textual retrieval at different levels. Graphiti emphasizes incremental episodic/temporal facts. These engines do not share one interchangeable API. Choose from the primary-source catalog and pin installed versions before coding; catalog presence is not runtime availability.

## Graph contracts
An entity has stable identity/type; a relation has endpoints, predicate, fact, source episode and validity history. A document or extraction proposal is not an established domain fact. Entity merging must retain all origins. Use documented invalidation/history rules for contradictory assertions. Never guess a relationship solely because two nodes are nearby in a layout.

## Live UI
Emit committed deltas with monotonically increasing event IDs. Snapshot and cursor must be transactionally consistent. Replay SSE after reconnect; preserve node positions and render bounded subgraphs, with search/filter/neighbor expansion and equivalent tabular content. The visualization latency target begins at graph commit, not at the start of LLM extraction.

## Failure and lifecycle
Maintain durable episode IDs, exclude partial indexes, and reconcile interrupted operations before retry. Use deterministic IDs where supported. Retire old document evidence and graph origins when updating/removing sources, preserving shared entities needed by other documents. Never replace a failed Graphiti call with invented relationships.
