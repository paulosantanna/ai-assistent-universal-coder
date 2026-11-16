# Verification ledger

Updated: 2026-10-15
Entry point: README.md. Owner: codenavi-agent.

## Actual runtime evidence

- Official MCP2.3 SDK negotiated2025-11-25;14tools, static resources and progressive source template verified through real stdio calls. Invalid inputs are rejected without echoing the canary input.
- Local Neo4j/Graphiti indexing, graph retrieval and cited Qwen answer completed. Source acquisition and complete graph indexing are separate: the graph is not claimed to contain every acquired document.
- CUDA13/Torch2.14.1 kernel, Qwen inference and official Laya typed inference passed on RTX5080/16GB.
- Edge desktop1440/mobile390 checks passed: live connection, catalog, graph, accessible table, no JS errors and no horizontal overflow. Browser evidence and screenshots remain local under .work/rag-graph-laya/.
-33primary sources/1256966characters acquired, including full papers and implementation contracts. Revisions/hashes/rights exclusions: knowledge/acquisition.manifest.json. Acquisition is not full semantic verification of every document.
- Nine retrieval measurements (three public queries × hybrid/graph/Laya) recovered the expected source in each case. Two documents were indexed at comparison time; current graph coverage is in verification.json. Fixed order and cold/warm effects prohibit a performance ranking.

## Training and limits

Dataset6e1072d3904f46339bddd3ee718d1b0b contains2000examples per flow with1600/200/200family-disjoint partitions;100examples per flow await human review. Extractive references preserve source provenance; template questions are correlated and their route/relevance labels are provisional. They are not2000independent human judgments.

- laya: completed2epochs; checkpoint reload and base/candidate validation completed. Experiment `29bcb81705714fe08d514c4fc09aab7e`; exact metrics/checkpoint hashes in verification.json. No promotion.
- llm: completed2epochs; checkpoint reload and base/candidate validation completed. Experiment `a61b06bb89124da9bbe23b0fc915527f`; exact metrics/checkpoint hashes in verification.json. No promotion.

Laya validation accuracy/ECE and LLM reference-token-F1/citation-format/negative-abstention are separate metrics. Synthetic validation scores cannot establish factual correctness or deployment accuracy. Human test review remains pending; no model is promoted.

The initial Laya worker rejected shorthand gold labels; the adapter now uses SDK expected labels and records native dry_run preprocessing. The initial QLoRA step failed in TRL1.15's unconditional Triton fused LM head; a real one-step reproduction passed with the public Trainer compute_loss extension using standard causal cross entropy. Original datasets/base weights remain intact.

## Reproducibility and boundaries

- Dependencies: uv.lock and hash-pinned requirements-core.lock/requirements-test.lock. Training uses the official CUDA index; protocol/CI does not require GPU/model weights.
- Java/Neo4j archives verified against official SHA256; Cytoscape pinned revision/hash with MIT license retained. Installed SDK signatures were verified instead of assuming GitHub main equals a published release.
- Credentials remain in Windows Credential Manager/runtime environment; corpus, datasets/checkpoints and provider state remain ignored. No paid model API, remote deployment, Git commit or push was performed.
- Local focused tests/quality gates are recorded in .work/rag-graph-laya/checks.json; their final status is reported at debrief. CI workflow changes are prepared; no remote CI success is inferred.
