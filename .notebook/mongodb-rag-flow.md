# MongoDB-backed RAG flow review
Updated: 2026-10-15
Entry point: rag-graph-laya-mcp/docs/mongodb-review/README.md.

- Read-only inspector: rag-graph-laya-mcp/scripts/review_mongodb.js; mongosh already installed at D:/MongoDB/mongosh/bin. Configuration points to local27017/data; do not open raw WiredTiger files in another instance.
- Original project code: 02_repositorios/DiabeticsresearchJEV/src/diabeticsresearchjev. Four controlled reproductions are distinct from the aggregate live-data receipt; the original review did not certify process/source correspondence; the subsequent source-local API startup verifies module paths/hashes and listener identity in docs/mongodb-review/typing-runtime-verification.json.
- Revised flow: source checkpoint → provenance/quality/use gates → chunks → equally filtered indexes/graph → committed projection → domain-calibrated Laya or hybrid → cited response; separate rights/disjoint human-review gates before RLCD/QLoRA/promotion.
- Source corrections R1–R6 are applied; current evidence: rag-graph-laya-mcp/docs/mongodb-review/{APPLIED.md,TYPING-RUNTIME.md,typing-runtime-verification.json}. Snapshot counts/transient readiness belong in the report/PROGRESS, not durable memory. Re-read live counts before resuming work.
- Evidence: docs/mongodb-review/{evidence.json,reproductions.json,verification.json}; no raw document values or credentials retained.
