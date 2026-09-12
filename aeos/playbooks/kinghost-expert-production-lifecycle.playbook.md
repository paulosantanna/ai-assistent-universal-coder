# Playbook: kinghost-expert-production-lifecycle

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
2. `kinghost_control.environment.select` (`local` | `staging` | `production`).
3. Open panel/wp-admin cookie via `runtime-auth`, or Playwright with that cookie; keep only `session_ref`.
4. Bind already-provisioned FTP/MySQL credentials through `kinghost_control.credential.bind` (`env_reference`, `secret_reference` or `runtime_memory`).
5. Advance FSM: `CREDENTIALS_BOUND` → `PANEL_AUTH` → `INVENTORY`.
6. If WordPress and no valid Beta Map exists, run `wordpress-expert` mapping-only first.
7. Snapshot remote scoped files; create `rollback_ref`.
8. Diff workspace vs remote; refuse WordPress core / `wp-config.php` without high-risk approval.
9. Dry-run FTP upload (`dry_run` default true).
10. APPLY only with `approved=true`, `change_id` and `rollback_ref`.
11. VERIFY with cookie or Playwright; layout changes need desktop and mobile.
12. On failure, ROLLBACK and close sessions.
13. On success, CLOSE credential/FTP/MySQL/auth sessions and return PASS with redacted evidence.

## Production PASS

PASS requires verified WordPress/PHP behavior after publish. FTP transfer success is not sufficient. No secret material in evidence.
