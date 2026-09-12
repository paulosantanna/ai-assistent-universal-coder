# HANDOFF

Updated: 2026-09-12

## Objective
- Add a deterministic KingHost control MCP and the `kinghost-expert` super-skill for WordPress/PHP production FTP publish.

## Last Verified State
- `kinghost-control` MCP smoke PASS. Overlay loads `kinghost-control`, `kinghost-commerce`, `kinghost-expert`, and `kinghost-expert-production-lifecycle`.
- Jest: `tests/node/kinghost-control-mcp.test.cjs` and overlay assertions in `tests/node/runtime-auth-broker.test.cjs` PASS.
- Runtime `tsc` build PASS. Skill frontmatter, skill-adapter, artifact-contract and full-workspace guards PASS.
- No live KingHost FTP/MySQL session was opened in this mission (no production credentials supplied).

## Working Set
- `kinghost-control-mcp/`
- `aeos/mcps/kinghost-control.mcp.yaml`
- `skills/kinghost-expert/`
- `aeos/playbooks/kinghost-expert-production-lifecycle.playbook.md`
- `runtime/src/kernel/kinghost-tool-router.ts`
- `aeos/registries/{overlay.registry.index.yaml,mcps.kinghost.additions.yaml,skills.kinghost-expert.additions.yaml,playbooks.kinghost-expert.additions.yaml}`

## Risks And Next Actions
- Production APPLY still needs operator-supplied env/secret refs or a cookie jar outside the workspace; this mission did not publish to KingHost.
- MySQL live queries require `npm run aeos:kinghost:deps` so `mysql2` exists under `kinghost-commerce-mcp`.
- Prior CI repair `8282a497` / run `34707694897` remains the last known green `master` SHA.

## Prior Local Storefront (unchanged)
- Runtime: `E:\GitHub\repos-workspace\reidoabc`. Reference package `reidoabc-wordpress` is read-only. Neither is deployed to KingHost.
