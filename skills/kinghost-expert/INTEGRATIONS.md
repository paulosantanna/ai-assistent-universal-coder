# KingHost panel, domain, user and WordPress session integrations

## Cookie

Use `kinghost_control.panel.session.open_cookie_file` with an absolute cookie-jar path outside the workspace (the workspace cookier file is consumed in place). Default hosts: `painel.kinghost.com.br`, `*.kinghost.com.br`, `king.host`, `*.kinghost.net`. `runtime-auth` `auth.session.open_cookie_file` remains valid for wp-admin and `runtime-http`.

## Domains

`kinghost_control.domain.list` then `domain.select`. Sources: `KINGHOST_DOMAINS` / `domains[]`, authenticated panel HTML, or FTP home directories. Always select an existing domain before clone or production publish.

## Already-created users

`kinghost_control.users.list` unions bound FTP/MySQL usernames, operator-supplied usernames and WordPress `wp_users` (email masked, no `user_pass`). Panel has no documented public account-user API; do not scrape passwords from Gerenciar FTP / Gerenciar usuários MySQL.

## Playwright / browser

Drive `https://painel.kinghost.com.br` or wp-admin with the same session to select domain, inspect PHP/MySQL/FTP/WordPress tools and smoke production. Do not capture password fields.

## FTP clone and publish

Bind with `kinghost_control.credential.bind`. Open FTP via `ftp.session.open` (`remote_root` typically `public_html` or `wp-content`). Clone: `site.clone` / `ftp.tree.download` (skips `wp-config.php`). Publish: `ftp.tree.upload` or `deploy.workspace_to_production` with dry-run default and mutation gates.

## MySQL / WooCommerce

`mysql.session.open` then `mysql.wordpress.inventory` / `wordpress.users.list` / `wordpress.plugins.inventory`. WooCommerce is a WordPress plugin under `wp-content/plugins/woocommerce`, not a KingHost product. Requires `mysql2` from `npm run aeos:kinghost:deps`. External MySQL needs the panel IP allowlist.
