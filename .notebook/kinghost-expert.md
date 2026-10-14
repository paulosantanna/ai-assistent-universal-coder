# KingHost control MCP and expert skill

Reconciled: 2026-10-12 — canonical skills are in `00_skills/`; removed AEOS runtime/configuration pointers below are historical, not current availability. See `tlc-skills.md`.


Entry: `00_skills/(cloud)/kinghost-expert/SKILL.md`, `aeos/mcps/kinghost-control.mcp.yaml`  
Updated: 2026-09-16

- Overlay registers `kinghost-control` MCP and `kinghost-expert` super-skill.
- One-command publish: playbook `kinghost-wordpress-publish` / `npm run aeos:kinghost:publish`.
- Panel login consumes an external cookie jar (`panel.session.open_cookie_file`); values never persist.
- Existing domains are listed/selected (`domain.list` / `domain.select`); `KINGHOST_DOMAINS` is the fail-closed fallback.
- Already-created FTP/MySQL/WordPress users are listed redacted; passwords never return.
- Site clone and production publish use FTP tree download/upload with dry-run, approval and rollback.
- WooCommerce is inventoried as a WordPress plugin plus MySQL tables, not a KingHost product API.
