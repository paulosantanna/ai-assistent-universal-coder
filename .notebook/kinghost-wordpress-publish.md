# KingHost one-command WordPress publish

Entry: `aeos/playbooks/kinghost-wordpress-publish.playbook.md`, `scripts/aeos-kinghost-publish.mjs`  
Updated: 2026-09-16

- Command: `npm run aeos:kinghost:publish -- --local-dir <tree> --domain <existing-domain>`
- Preflight: `kinghost_control.publish.preflight`
- Default: DRY_RUN of scoped `wp-content` (themes/plugins/mu-plugins)
- WooCommerce: publish plugin/theme code; preserve live orders, customers, payment secrets, siteurl/home
- APPLY: `--apply` + `AEOS_KINGHOST_APPROVED=true` + `change_id` + `rollback_ref`
- `--replace-database` is blocked on this path
