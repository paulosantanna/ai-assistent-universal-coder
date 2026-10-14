<!-- Package: 00_skills/(cloud)/kinghost-expert; relative command/resource examples resolve from that package or workspace root. -->

## Credential contract

Obtain already-provisioned logins from approved runtime sources. Do not invent, scrape, brute-force or persist passwords.

Approved sources:

1. environment variable references (`KINGHOST_FTP_USER`, `KINGHOST_FTP_PASSWORD`, MySQL equivalents, `KINGHOST_DOMAINS`);
2. approved secret-manager references materialized by `runtime-auth`;
3. ephemeral runtime memory supplied by the Tool Router;
4. KingHost panel cookie/cookie-jar file consumed in place via `kinghost_control.panel.session.open_cookie_file`.

The model/notebook may see opaque refs, usernames, host, port, domain and environment id when necessary. They must never see passwords, raw cookies, nonces, `user_pass` hashes, mailbox secrets or `wp-config.php` secrets.
