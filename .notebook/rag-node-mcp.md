# rag-node-mcp

Entry point: `aeos/mcps/rag-node.mcp.yaml`, server `aeos/mcp-servers/rag-node-mcp.mjs`
Updated: 2026-09-18

- Offline governed MCP implementing the public TLC `RAG com Node.js` outline (9 aulas, 3 seções).
- Tools: `rag_node.health|curriculum|ingest|search|chat|express_plan`; hybrid TF-IDF cosine + lexical, stable `${docId}#c${i}` chunks, refusal on weak grounding, Express + SSE plan.
- Intake lenses (not agents): `voiceai` (`skills/voiceai/SKILL.md`) for literal transcript + handoff; `aura-voice` (`aeos/skills/generated/aura-voice.skill.md`) for local transcription + term preservation + humor/serious split.
- Verbatim lesson video absorption is BLOCKED until the user supplies authorized media; MCP answers from `public-outline-only` plus open Node RAG standards.
- Registry: `aeos/registries/mcps.rag-node.additions.yaml` (governed by `rag-expert`), indexed in `overlay.registry.index.yaml`. Test: `tests/node/rag-node-mcp.test.cjs`.
