# Complete WordPress plugin universe

Entry: `skills/wordpress-expert/SKILL.md`  
Updated: 2026-09-16

`wordpress-expert` uses the **entire installed plugin set** of the target WordPress tree. It does not limit work to WooCommerce or any static catalog.

## Source of truth

Inventory from the site, not from a guessed list:

1. `wp-content/plugins/` — directory plugins and single-file plugins;
2. `wp-content/mu-plugins/` — must-use plugins;
3. remote `active_plugins` / `woocommerce` and other options only as activation state, never as the installed set;
4. KingHost FTP listing of `wp-content/plugins` when operating a hosted site.

A static directory catalog (WooCommerce, Jetpack, Elementor, …) is a hint, never a cap.

## What “use all plugins” means

- Map every installed slug (active, inactive, must-use) into the Beta Map `plugins[]`.
- Treat custom, official-directory and e-commerce plugins as first-class extension points.
- Include the full local `wp-content/plugins` and `wp-content/mu-plugins` trees in `kinghost-wordpress-publish`.
- Activate/deactivate/update only the plugins required by the requested change, under existing production gates.
- Consult `wordpress-knowledge` Plugin Handbook and `https://wordpress.org/plugins/` for third-party plugin APIs. Plugin-specific secrets stay out of evidence.

## Local inventory

`kinghost-control-mcp/wordpress-ops.mjs:listLocalWordpressPlugins()` and `inspectLocalWordpressTree()` return every discovered slug. Preflight `kinghost_control.publish.preflight` exposes that list.

## Publish

Default KingHost APPLY uploads all local plugin files under `wp-content/plugins` and `wp-content/mu-plugins`. Live commerce data, payment secrets, `siteurl`/`home` and `wp-config.php` remain production-owned.

## Never

- Invent plugins that are not in the tree or remote listing.
- Sample only “popular” plugins into the Beta Map.
- Dump `option_value` gateway keys or `user_pass`.
- Edit WordPress core to compensate for a missing plugin.
