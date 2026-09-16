# KingHost control MCP and expert skill

Entry: `skills/kinghost-expert/SKILL.md`, `aeos/mcps/kinghost-control.mcp.yaml`  
Updated: 2026-09-16

- Overlay registers `kinghost-control` MCP and `kinghost-expert` super-skill.
- Panel login consumes an external cookie jar (`panel.session.open_cookie_file`); values never persist.
- Existing domains are listed/selected (`domain.list` / `domain.select`); `KINGHOST_DOMAINS` is the fail-closed fallback.
- Already-created FTP/MySQL/WordPress users are listed redacted; passwords never return.
- Site clone and production publish use FTP tree download/upload with dry-run, approval and rollback.
- WooCommerce is inventoried as a WordPress plugin plus MySQL tables, not a KingHost product API.
