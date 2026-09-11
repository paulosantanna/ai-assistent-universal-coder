# One-Shot Beta Mapping

## Purpose

Build the durable structural model required for future WordPress changes without repeatedly crawling the entire site.

## Trigger

Run full mapping only when `.aeos/wordpress/sites/<site-id>/beta-map.json` is absent or invalid. A consolidated valid map suppresses automatic full remapping forever unless explicit `remap` intent is given.

## Read-only mapping stages

1. canonical URL, HTTPS, redirects, WordPress detection;
2. authenticated cookie-session validation and wp-admin reachability;
3. WordPress/core version and REST index/namespaces;
4. block/classic theme architecture, active theme and parent/child topology;
5. plugins, versions and activation state;
6. post types, taxonomies, page/post IDs/counts/status summaries;
7. navigation/menus, templates, template parts, patterns and widgets/sidebars where applicable;
8. safe site settings/permalink metadata;
9. front-end CSS/JS/font/image asset inventory and builders/framework indicators;
10. custom REST namespaces, integrations and external domains;
11. cache/CDN/security/backup/deployment affordances;
12. role/capability summary without usernames/emails or unnecessary personal data;
13. risk register and recommended mutation surfaces.

## Persisted schema intent

Persist architecture and identifiers, not secrets or copied site content. Store only the auth mode/provider alias, never cookie path contents or nonce.

## Subsequent runs

Run only:

- target URL check;
- WordPress version drift;
- active theme/plugin drift;
- REST namespace drift;
- requested-resource freshness;
- backup/rollback availability;
- current authenticated capability for the planned operation.

Do not rebuild the whole map automatically.
