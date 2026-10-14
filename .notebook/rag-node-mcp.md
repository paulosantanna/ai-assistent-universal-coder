# rag-node-mcp

Entry point: `aeos/mcps/rag-node.mcp.yaml`, server `aeos/mcp-servers/rag-node-mcp.mjs`
Updated: 2026-09-18

- Offline governed MCP implementing and explaining the TLC `RAG com Node.js` model from the public outline, complete source repository history and current official docs.
- Course evidence: `https://github.com/odanieldcs/rag-api` at `27f7aab`; 22 tracked files and 12 commits inspected (`d09e969..27f7aab`).
- Architecture: predictable 2-Step RAG. Indexing: PDF → pages → 1000/200 chunks → metadata → `text-embedding-3-small` 1536d → Qdrant Cosine. Query: validate → query embedding → topK → context → `gpt-4o-mini` → sources. Serving: Express routes + SSE.
- Knowledge map: `aeos/knowledge/rag-node-course-map.json` stores the causal map for all 12 commits, file responsibilities, stack decisions, 12 production gaps and official evidence.
- Tools: runtime `health|curriculum|ingest|search|chat|express_plan`; knowledge `architecture|evolution|why|production_gaps|sources`.
- Course baseline gaps that must not be copied blindly: no relevance threshold, auth/ACL filters, injection validation, tests/evals or document lifecycle; ESM `require` defect; undeclared direct LangChain imports; citation mismatch; unsafe wildcard CORS; SSE client framing/disconnect defects.
- Official evidence checked 2026-09-18: LangChain retrieval/knowledge-base/RAG security, OpenAI embeddings/model, Qdrant collections/search/indexing, MDN SSE/Fetch and Express 5 error handling.
- Verbatim transcripts were not needed for this revision and are not claimed as evidence.
- Registry: `aeos/registries/mcps.rag-node.additions.yaml` (governed by `rag-expert`), indexed in `overlay.registry.index.yaml`. Test: `tests/node/rag-node-mcp.test.cjs`.
