# Playbook: kinghost-expert-production-lifecycle

General KingHost production FSM. For an already-altered local WordPress/WooCommerce tree on an already-hosted domain, use `kinghost-wordpress-publish` (`npm run aeos:kinghost:publish`) instead of this playbook.

## Required agent

- `codenavi-agent` only.

## Required skill

- `kinghost-expert`

## Required MCPs

- `runtime-auth` (core-injected)
- `runtime-http` (core-injected)
- `kinghost-control`
- `wordpress-knowledge`
- `browser`
- `filesystem-readonly`

## Flow

1. Read continuity and resolve workspace WordPress/PHP tree plus target KingHost site.
2. Open the panel cookie jar with `kinghost_control.panel.session.open_cookie_file` (absolute path outside Git). Keep only `panel_session_ref`.
3. `kinghost_control.domain.list` then `domain.select` for an existing Hospedagem domain. `KINGHOST_DOMAINS` is an allowed fallback.
4. `kinghost_control.environment.select` (`local` | `staging` | `production`) including the selected domain.
5. Bind already-provisioned FTP/MySQL credentials through `kinghost_control.credential.bind` (`env_reference`, `secret_reference` or `runtime_memory`).
6. `users.list` / `wordpress.users.list` for already-created identities (redacted). Inventory plugins including WooCommerce.
7. Advance FSM: `CREDENTIALS_BOUND` → `PANEL_AUTH` → `INVENTORY`.
8. If the local tree is missing, `site.clone` (dry-run first; skip `wp-config.php`).
9. If WordPress and no valid Beta Map exists, run `wordpress-expert` mapping-only first.
10. Snapshot remote scoped files; create `rollback_ref`.
11. Diff workspace vs remote; refuse WordPress core / `wp-config.php` without high-risk approval.
12. Dry-run `ftp.tree.upload` or `deploy.workspace_to_production` (`dry_run` default true).
13. APPLY only with `approved=true`, `change_id` and `rollback_ref`.
14. VERIFY with cookie or Playwright; layout changes need desktop and mobile.
15. On failure, ROLLBACK and close sessions.
16. On success, CLOSE credential/FTP/MySQL/panel sessions and return PASS with redacted evidence.

## Production PASS

PASS requires verified WordPress/PHP behavior after publish. FTP transfer success is not sufficient. No secret material in evidence.
