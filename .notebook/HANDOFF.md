# HANDOFF

Updated: 2026-09-18

## Objective
- Use `aura-voice` (aurea) and `voiceai` (vox) as intake lenses, absorb the TLC RAG-com-Node.js lessons and ship a governed RAG MCP for Node.js/Express.

## Last Verified State
- `rag-node` MCP defined at `aeos/mcps/rag-node.mcp.yaml` with stdio server `aeos/mcp-servers/rag-node-mcp.mjs`.
- Active through overlay fragment `aeos/registries/mcps.rag-node.additions.yaml` (governed by `rag-expert`).
- `npm run aeos:verify` PASS (14 suites / 78 tests), including new `tests/node/rag-node-mcp.test.cjs` (4 tests).
- Branch: `cursor/rag-node-mcp-27ce` (this session). Paulo declarou em 2026-09-18 ser comprador do curso e autorizar o uso do conteúdo; os arquivos/transcritos das aulas ainda não foram entregues, então a absorção verbatim segue BLOCKED até o handoff das fontes.

## Working Set
- `aeos/mcps/rag-node.mcp.yaml`
- `aeos/mcp-servers/rag-node-mcp.mjs`
- `aeos/registries/mcps.rag-node.additions.yaml`
- `aeos/registries/overlay.registry.index.yaml`
- `tests/node/rag-node-mcp.test.cjs`
- `.notebook/rag-node-mcp.md`, `.notebook/INDEX.md`, `.notebook/PROGRESS.md`

## Risks And Next Actions
- Paulo entrega as fontes autorizadas (ver formato abaixo); então rodo `voiceai` transcrição literal mais `aura-voice` preservação de termos e separação humor/sério, e estendo `rag_node.curriculum` além do outline público.
- Formato do handoff: arquivos de mídia/transcrito fornecidos pelo usuário dentro do workspace (ex. `.aeos/sandbox/rag-tlc/<aula>.mp4|.mp3|.srt|.vtt|.txt|.md`) ou path montado fornecido por ele, um por aula, com título da aula. Não usar login/senha nem cookies do TLC; o link da página do curso sozinho não entrega os vídeos porque o acesso é gated por sessão.
- Não commitar transcritos verbatim do curso no repo público; mantê-los como evidência local não rastreada e commitar só o mapeamento destilado.
- Next: commit, push `cursor/rag-node-mcp-27ce`, open PR with Why/Porquê, then optionally add an Express reference app consuming `rag_node.express_plan`.
