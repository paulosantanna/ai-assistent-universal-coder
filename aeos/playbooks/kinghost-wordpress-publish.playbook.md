# Playbook: kinghost-wordpress-publish

## Objective

Publish a locally altered PHP/WordPress site (including WooCommerce and other plugins) onto an already-hosted KingHost Hospedagem domain with one AI/operator command. Production remains the source of truth for live commerce data. The local tree is the source of truth for scoped `wp-content` code.

## Version

1.0.0

## One command

```bash
npm run aeos:kinghost:publish -- --local-dir <wordpress-tree> --domain <existing-kinghost-domain>
```

That is DRY_RUN/preflight. APPLY is the same command plus `--apply`, `AEOS_KINGHOST_APPROVED=true`, `--change-id` and `--rollback-ref`.

AI utterance that must run this playbook (do not invent a second procedure):

- `publique o site no KingHost`
- `publish the WordPress/WooCommerce site to KingHost`

## Required agent

- `codenavi-agent` only.

## Required skills

- `kinghost-expert` (governing)
- `wordpress-expert` when a WordPress Beta Map is missing or drift is material

## Required MCPs

- `runtime-auth` (core-injected)
- `runtime-http` (core-injected)
- `kinghost-control`
- `wordpress-knowledge`
- `browser`
- `filesystem-readonly`

## Required LCPs

- `global-rules`
- `security-governance`

## Preconditions

- Target domain already exists on KingHost Hospedagem.
- Local WordPress/PHP tree already contains the intended changes.
- FTP (and optional MySQL/wp-admin) usernames already exist; passwords come from env/secret/runtime memory, never from scraping.
- Panel cookie jar, if used, is an absolute path outside Git (`KINGHOST_COOKIE_JAR`).
- Production APPLY requires dry-run evidence, `approved=true`, `change_id` and `rollback_ref`.

## Inputs

| Input | Required | Notes |
| --- | --- | --- |
| `--local-dir` | yes | Local WordPress root or `wp-content` |
| `--domain` | yes for APPLY | Must appear in `domain.list` / `KINGHOST_DOMAINS` |
| `--environment` | no | `local` \| `staging` \| `production` (default `production`) |
| `--include-uploads` | no | Default false; media is large and rarely needed for code publish |
| `--replace-database` | no | Default false; high-risk; never default for WooCommerce shops |
| `--apply` | no | Default false (DRY_RUN) |

## WooCommerce / plugin policy

Default APPLY uploads scoped code only:

- `wp-content/themes`
- `wp-content/plugins` (custom and requested plugin files, including WooCommerce plugin files when present locally)
- `wp-content/mu-plugins`

Default APPLY does **not** overwrite production:

- orders (`wc_orders` / `shop_order`)
- customers
- payment gateway secrets in options
- `siteurl` / `home`
- `wp-config.php`, `wp-admin/`, `wp-includes/`
- `user_pass` hashes

Product catalog SQL and `wp-content/uploads` require explicit high-risk approval. After WooCommerce page assignment, verify the public routes (`/cart/`, `/checkout/`, `/my-account/`, `/shop/`), not only `woocommerce_*_page_id`.

## Steps

1. Run `npm run aeos:kinghost:publish -- --local-dir … --domain …` (or `kinghost_control.publish.preflight`) and stop if the local tree is not WordPress/PHP.
2. `kinghost_control.knowledge_search` for FTP, domain, WooCommerce and clone/deploy facts.
3. Open the panel cookie jar when `KINGHOST_COOKIE_JAR` is set. Keep `panel_session_ref` only.
4. `domain.list` then `domain.select` for the existing hosting domain.
5. `environment.select` (`local` \| `staging` \| `production`) including that domain.
6. Bind already-created FTP (and optional MySQL) credentials as opaque refs.
7. Advance FSM: `CREDENTIALS_BOUND` → `PANEL_AUTH` → `INVENTORY`.
8. Inventory remote plugins/themes and WooCommerce tables. Do not dump option secrets.
9. If a WordPress Beta Map is missing, run `wordpress-expert` mapping-only, then continue only with explicit same-run publish authorization.
10. Snapshot remote scoped files; create `rollback_ref`. Skip `wp-config.php`.
11. Diff local scoped tree vs remote. Refuse core / `wp-config.php` without `high_risk_approved`.
12. Dry-run `deploy.workspace_to_production` or `ftp.tree.upload` (`dry_run` default true). Default `remote_root` is `wp-content`.
13. APPLY only with `approved=true`, `change_id`, `rollback_ref` and `--apply`. SQL replacement stays blocked unless `--replace-database` and high-risk approval.
14. VERIFY with cookie or Playwright: homepage, wp-admin identity when bound, and WooCommerce routes when the plugin is active. Layout changes need desktop and mobile.
15. On failure, ROLLBACK and CLOSE sessions.
16. On success, CLOSE sessions and return PASS with redacted evidence.

## Blocking conditions

- Domain not in the existing KingHost inventory.
- Missing FTP bind material (env/secret/runtime memory).
- Local tree missing or not a WordPress/PHP layout.
- Production mutation without dry-run, approval, change_id or rollback_ref.
- Attempt to upload `wp-config.php` or WordPress core without high-risk approval.
- Attempt to replace live WooCommerce orders/customers/payment secrets as part of a normal publish.
- Credential discovery, password dump or cookie persistence requested.
- Smoke/VERIFY failure.

## Required evidence

- preflight record (layout, scopes, WooCommerce policy, present env **names** only)
- selected domain and environment
- dry-run FTP file list
- rollback_ref
- redacted change_id
- VERIFY URLs and outcomes (no cookies, no passwords)

## Rollback strategy

Re-upload the SNAPSHOT tree, restore SQL only if SQL was mutated, purge cache, repeat smoke. `ROLLBACK` is legal from `APPLY` or `VERIFY` failure.

## Judge requirements

PASS requires verified resulting WordPress/PHP/WooCommerce HTTP behavior after publish. FTP `226` / transfer success is not sufficient. No secret material in evidence.

## Relationship

- `kinghost-expert-production-lifecycle` remains the general KingHost FSM playbook (clone-if-missing and arbitrary production work).
- This playbook is the one-command path when the local site is already altered and the KingHost domain already hosts WordPress/PHP.
