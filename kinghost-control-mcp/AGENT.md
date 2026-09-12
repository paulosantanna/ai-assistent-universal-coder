# KingHost Control MCP adapter contract

Governance: CodENavi Full Workspace v2

Inherits root `AGENT.md` and `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`.

All adapter operations follow **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**.

Specific rules:

- this adapter is deterministic: environment selection, credential bind, FTP and production FSM follow fixed state order;
- credentials are resolved from approved runtime sources (env, secret reference, cookie/Playwright panel bind) and never printed;
- opaque `credential_ref` / `session_ref` values are the only identifiers returned to skills;
- WordPress core, `wp-config.php` and unscoped `public_html` writes are blocked unless high-risk approved;
- FTP mutations require `approved=true`, `change_id`, dry-run evidence and `rollback_ref`;
- MySQL mutations require EXPLAIN/read-first posture and the same mutation gates;
- panel/wp-admin authentication uses external cookie files or Playwright through runtime-auth; cookie contents never persist;
- undocumented KingHost private APIs are unsupported and must fail closed.
