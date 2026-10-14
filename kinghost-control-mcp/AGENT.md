# KingHost Control MCP adapter contract

Governance: CodENavi Full Workspace v2

Inherits root `AGENT.md` and `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`.

All adapter operations follow **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**.

Specific rules:

- this adapter is the KingHost Hospedagem control plane: cookie-jar panel login, domain list/select, already-created users, WordPress/PHP/MySQL/WooCommerce inventory, site clone and FTP production publish;
- credentials are resolved from approved runtime sources (env, secret reference, cookie/Playwright panel bind) and never printed;
- opaque `credential_ref` / `session_ref` / `panel_session_ref` values are the only identifiers returned to skills;
- WordPress core, `wp-config.php` and unscoped `public_html` writes are blocked unless high-risk approved;
- FTP mutations require `approved=true`, `change_id`, dry-run evidence and `rollback_ref`;
- MySQL mutations require EXPLAIN/read-first posture and the same mutation gates;
- panel authentication uses an external cookie-jar consumed in place; cookie contents never persist or return to the model;
- domain listing uses operator/env inventory, cookie-authenticated GET of `https://painel.kinghost.com.br`, or FTP directories — never an invented private API;
- undocumented KingHost private APIs are unsupported and must fail closed.
