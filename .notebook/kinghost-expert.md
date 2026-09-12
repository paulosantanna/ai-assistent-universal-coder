# KingHost control MCP and expert skill

Entry: `skills/kinghost-expert/SKILL.md`, `aeos/mcps/kinghost-control.mcp.yaml`  
Updated: 2026-09-12

- Overlay registers `kinghost-control` MCP and `kinghost-expert` super-skill (`aeos/registries/overlay.registry.index.yaml`).
- Credentials bind as opaque `credential_ref` from env/secret/runtime memory or cookie-panel plan; passwords never persist.
- Production publish is the FSM in `skills/kinghost-expert/PRODUCTION_FSM.md` plus KingHost FTP (`kinghost-control-mcp`).
- Cookie or Playwright authenticates KingHost panel / wp-admin through `runtime-auth` / `browser`.
