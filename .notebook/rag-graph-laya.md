# GraphRAG + Laya
Updated: 2026-10-15
Entry point: rag-graph-laya-mcp/README.md.

- Official SDK stdio server uses MCP2.3 constructor handlers and negotiates2025-11-25.14tools plus source catalog/synthesis and progressive source passages. Inventory: quality/capabilities.json; schemas: app/contracts.py.
- A single local API owns persistent jobs/events/models. Stdio clients proxy it; protocol probing works without credentials/weights. Graphiti/Neo4j changes are mirrored after commit; snapshot/cursor is transactional and SSE replays from IDs.
- Laya supplies bounded typed decisions; uncalibrated, uncertain or truncated requests retain hybrid fallback. LLM generation validates citation IDs; semantic entailment remains a separate evaluation.
- Windows runtime profile is isolated Python3.12/CUDA13. Neo4j credential provider: CodENavi/GraphRAG-Laya/Neo4j, outside tracked state. Source corpus/datasets/checkpoints stay ignored; no paid APIs enabled by default.
- Laya scalar labels use expected; gold requires distributions. Native dry_run checks preprocessing. Windows TRL1.15 fused loss requires unavailable Triton; portable_sft.py uses the public Trainer causal-CE loss extension with the same QLoRA/completion labels.
- Four skills live in 00_skills/(development), with <=100physical entry lines and local references. rag-laya-expert composes the other three; no new identities.
- Source/license evidence and acquisition scope: knowledge/acquisition.manifest.json and sources.json. Measured training and verification scope: verification.json/VERIFICATION.md. Synthetic template labels and acquisition do not establish human-reviewed domain expertise; no automatic promotion.
