# HANDOFF

Updated: 2026-09-16

## Objective
- Complete KingHost Hospedagem control MCP so cookie-jar login, domain list/select, already-created users, WordPress/PHP/MySQL/WooCommerce, site clone and production FTP publish are executable.

## Last Verified State
- `kinghost-control` v1.1 adds panel cookie bind, domain inventory, redacted user listing, FTP tree clone/upload and searchable hosting knowledge.
- Jest/Mocha 9/9, control smoke and `aeos:kinghost:smoke` passed.
- Live KingHost panel/FTP/MySQL against a real account is not verified in this environment.
- Draft PR: https://github.com/paulosantanna/ai-assistent-universal-coder/pull/42

## Working Set
- `kinghost-control-mcp/`
- `aeos/mcps/kinghost-control.mcp.yaml`
- `skills/kinghost-expert/`
- `tests/node/kinghost-control-mcp.test.cjs`

## Risks And Next Actions
- Verify with a real external cookie jar + FTP/MySQL env binds on an authorized account.
- Confirm panel HTML domain extraction against the current painel.kinghost.com.br markup; `KINGHOST_DOMAINS` remains the fail-closed fallback.
