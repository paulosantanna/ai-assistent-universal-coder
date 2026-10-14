<!-- Package: 00_skills/(development)/wordpress-expert; relative command/resource examples resolve from that package or workspace root. -->

## Complete plugin universe

The installed plugin set of the target site is first-class. Procedure: `00_skills/(development)/wordpress-expert/PLUGINS.md`.

- Inventory every slug in `wp-content/plugins` and `wp-content/mu-plugins` (active, inactive and must-use).
- Do not cap work at WooCommerce or a static popular-plugin list.
- Consult `wordpress-knowledge` (`plugin_universe_plan`, Plugin Handbook, `https://wordpress.org/plugins/`) before material third-party plugin API claims.
- Local inventory: `listLocalWordpressPlugins` / `inspectLocalWordpressTree`.
- KingHost publish (`kinghost-wordpress-publish` / `npm run aeos:kinghost:publish`) includes the full local plugin trees with the theme. Live orders, customers, payment secrets and `wp-config.php` stay on production.
