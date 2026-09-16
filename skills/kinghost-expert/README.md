# kinghost-expert

Super-skill of `codenavi-agent` for KingHost Hospedagem.

- MCP: `kinghost-control`
- Auth: external cookie jar (`panel.session.open_cookie_file`) or Playwright
- Domains: list and select existing hosting domains
- Users: already-created FTP/MySQL/WordPress identities, redacted
- Clone: FTP tree download to the workspace (skips `wp-config.php`)
- Publish: KingHost FTP tree upload with dry-run, approval, backup and rollback
- Credentials: bind already-created logins; never persist or print passwords
