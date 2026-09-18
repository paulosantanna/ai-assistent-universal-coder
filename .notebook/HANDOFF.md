# HANDOFF

Updated: 2026-09-18

## Objective
- Use `aura-voice` (aurea) and `voiceai` (vox) as intake lenses, absorb the TLC RAG-com-Node.js lessons and ship a governed RAG MCP for Node.js/Express.

## Last Verified State
- `rag-node` MCP defined at `aeos/mcps/rag-node.mcp.yaml` with stdio server `aeos/mcp-servers/rag-node-mcp.mjs`.
- Active through overlay fragment `aeos/registries/mcps.rag-node.additions.yaml` (governed by `rag-expert`).
- `npm run aeos:verify` PASS (14 suites / 78 tests), including new `tests/node/rag-node-mcp.test.cjs` (4 tests).
- Branch: `cursor/rag-node-mcp-27ce` (this session). Verbatim TLC video absorption stays BLOCKED until Paulo supplies authorized lesson media/transcripts via `voiceai`/`aura-voice`.

## Working Set
- `aeos/mcps/rag-node.mcp.yaml`
- `aeos/mcp-servers/rag-node-mcp.mjs`
- `aeos/registries/mcps.rag-node.additions.yaml`
- `aeos/registries/overlay.registry.index.yaml`
- `tests/node/rag-node-mcp.test.cjs`
- `.notebook/rag-node-mcp.md`, `.notebook/INDEX.md`, `.notebook/PROGRESS.md`

## Risks And Next Actions
- If Paulo provides authorized TLC lesson audio/video/transcripts, run them through `voiceai` literal transcription plus `aura-voice` term-preservation review, then extend `rag_node.curriculum` evidence beyond the public outline.
- Next: commit, push `cursor/rag-node-mcp-27ce`, open PR with Why/Porquê, then optionally add an Express reference app consuming `rag_node.express_plan`.
