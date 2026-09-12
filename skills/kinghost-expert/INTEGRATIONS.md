# KingHost panel and WordPress session integrations

## Cookie

Use `runtime-auth` `auth.session.open_cookie_file` with an absolute cookie-jar path outside the workspace. Scope hosts to `king.host` / `*.kinghost.com.br` for panel work and to the site hostname for wp-admin.

## Playwright / browser

Drive the KingHost panel or wp-admin with the same session to select environment, inspect PHP/MySQL/FTP tools and smoke production. Do not capture password fields into screenshots or logs.

## FTP / MySQL

Bind with `kinghost_control.credential.bind` using `source_class: env_reference` or `runtime_memory`. Open FTP via `kinghost_control.ftp.session.open`. MySQL uses the same bind then `kinghost_control.mysql.session.open` (requires `mysql2` from `npm run aeos:kinghost:deps`).
