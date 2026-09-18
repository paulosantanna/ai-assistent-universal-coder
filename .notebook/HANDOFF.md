# HANDOFF

Updated: 2026-09-18

## Objective
- Analyze the complete TLC `rag-api` repository, explain why each implementation step exists, and store the causal model plus current official evidence in the governed `rag-node` MCP.

## Last Verified State
- `rag-node` 1.1.0 is defined at `aeos/mcps/rag-node.mcp.yaml` with stdio server `aeos/mcp-servers/rag-node-mcp.mjs`.
- Active through overlay fragment `aeos/registries/mcps.rag-node.additions.yaml` (governed by `rag-expert`).
- Source evidence covers all 22 tracked files and 12 commits of `https://github.com/odanieldcs/rag-api` at `27f7aab`.
- `aeos/knowledge/rag-node-course-map.json` contains the 2-Step architecture, 12 causal commits, stack/file why map, 12 production gaps and 11 current official sources.
- Focused `tests/node/rag-node-mcp.test.cjs` PASS (6 tests); full `npm run aeos:verify` is the next gate.

## Working Set
- `aeos/mcps/rag-node.mcp.yaml`
- `aeos/mcp-servers/rag-node-mcp.mjs`
- `aeos/knowledge/rag-node-course-map.json`
- `aeos/registries/mcps.rag-node.additions.yaml`
- `aeos/registries/overlay.registry.index.yaml`
- `tests/node/rag-node-mcp.test.cjs`
- `.notebook/rag-node-mcp.md`, `.notebook/INDEX.md`, `.notebook/PROGRESS.md`

## Risks And Next Actions
- Run full verification, then commit/push and update PR #48.
- The repository is an educational baseline, not production-ready: highest risks are absent relevance thresholds, auth/ACL filtering and indirect prompt-injection validation. See `rag_node.production_gaps`.
- Recheck official APIs before implementing upgrades; the knowledge file records source URLs and an evidence date rather than freezing unverified signatures.
