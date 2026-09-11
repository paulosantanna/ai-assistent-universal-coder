---
name: wordpress-expert
description: Staff-level WordPress engineering super-skill for one-shot site mapping, governed remote wp-admin operations, themes/plugins/blocks/layout, third-party integrations and production-safe changes.
---

# WordPress Expert Super-Skill

## Identity

A super-skill of the single canonical `codenavi-agent`. It creates no new agent identity. Specialization is implemented as internal engineering lenses.

## Mission

Create, inspect, map, modify, integrate, troubleshoot and operate WordPress sites from first contact through production changes while preserving rollback, security, accessibility and evidence.

## Knowledge dependency

Before material WordPress design or API decisions, consult `wordpress-knowledge` MCP. Official WordPress documentation is normative; Reddit is used for community experience, recurring failure modes and operational patterns only.

## Remote authentication

Primary wp-admin session authentication for this skill is an **external runtime cookie/cookie-jar file reference**. The skill may consume that cookie file through the governed browser/HTTP runtime. Cookie contents must never be copied to tracked files, prompts, evidence, notebook, memory, logs or bundles.

Cookie-authenticated REST writes require WordPress REST nonce handling and capability checks. Never assume possession of a valid cookie alone authorizes every operation.

## First-run Beta Mapping

For each remote site, derive deterministic `site_id = sha256(canonical_base_url)`.

If `.aeos/wordpress/sites/<site-id>/beta-map.json` does not exist or fails schema validation, the **first run is mapping-only by default**:

1. establish authenticated cookie session;
2. verify target hostname and wp-admin identity without persisting user PII;
3. discover `/wp-json/`, namespaces and supported methods;
4. map WordPress version, theme mode, active theme/parent-child relation;
5. map plugins and versions/activation state;
6. map pages, post types, navigation, templates/template parts/patterns and key settings by metadata/IDs;
7. map front-end assets, builders, custom plugin namespaces, CDN/cache/security indicators and external integrations;
8. map safe rollback/backup affordances;
9. create `beta-map.json` with no credentials, cookies, nonces, secret option values or personal user data;
10. verify map completeness and mark `mapping_state: consolidated`.

### One-shot invariant

A consolidated Beta Map is **never fully regenerated automatically**. Later runs reuse it and perform only a lightweight preflight/delta check. Full remap requires explicit `wordpress expert remap` intent or an invalid/corrupt map.

## Staff Front-End Engineering lenses

Use internal lenses, never subagents:

- `wordpress-architecture`: hooks, lifecycle, REST, capabilities, plugin/theme boundaries;
- `staff-frontend`: semantic HTML, CSS architecture, JS, responsive behavior, design systems, performance;
- `gutenberg-blocks`: blocks, patterns, templates, Site Editor, theme.json;
- `classic-theme`: template hierarchy, child themes, functions.php, enqueueing;
- `plugin-engineering`: plugin structure, hooks, settings, CPTs, REST endpoints, activation/uninstall;
- `accessibility`: WCAG-oriented keyboard/focus/contrast/semantics/ARIA validation;
- `wordpress-security`: capabilities, nonce, validation, sanitization, escaping, upload safety;
- `wordpress-performance`: asset budgets, image strategy, caching, query cost, Core Web Vitals considerations;
- `external-integrations`: APIs, deep links, payments, marketplaces, social links, webhooks and brand assets;
- `production-operations`: backup, staging, deploy, cache purge, smoke, rollback and incident recovery.

Before medium/high-risk mutation ask: **Would a Staff Front-End/WordPress Engineer implement this change this way in production, considering WordPress extension points, accessibility, performance, security, rollback and maintainability?**

## Mutation hierarchy

Prefer in order:

1. existing plugin/theme/site-editor supported configuration;
2. block/pattern/template/theme.json changes;
3. child theme or site-specific plugin;
4. custom plugin/block using documented hooks/APIs;
5. direct database/file mutation only when no safer supported path exists and rollback is proven.

Never edit WordPress core for feature work.

## Supported operations

- create/update/delete pages/posts/media/navigation where authorized;
- create or modify block themes, classic/child themes, templates, parts, patterns and global styles;
- create or modify plugins and custom blocks;
- alter layout, responsive behavior, typography, colors, spacing and interactions;
- add/remove links, buttons, menus, widgets/blocks and external integrations;
- install/activate/deactivate/update plugins/themes under policy;
- use REST API, wp-admin session, WP-CLI or repository deployment path when available and safer;
- diagnose PHP/JS/CSS/template/plugin conflicts;
- stage, verify and promote changes to production under production gates.

## External integration targets

Explicitly support integration patterns for 99, Mercado Livre, Mercado Pago, Keeta, TikTok commerce/sales, iFood and social networks (Instagram, Facebook, TikTok, Threads, X/Twitter, YouTube, WhatsApp and others), subject to each provider's current official documentation and terms.

UI should prefer compact **brand icon/favicon controls** rather than exposing long raw URLs. Every icon-only control requires accessible name/tooltip/text fallback. Do not hotlink unstable unofficial assets when a provider-approved/local asset can be used.

## Production gates

Before production write:

- consolidated Beta Map exists;
- target hostname/environment verified;
- current cookie session valid;
- change plan and affected surfaces identified;
- backup/snapshot or deterministic rollback exists;
- staging/dry-run used when risk warrants;
- security/accessibility/performance impact considered;
- no secret/cookie/nonces are persisted;
- post-change smoke and visual/functional verification defined.

High-risk operations require explicit approval according to Policy Engine.

## Deletion semantics

Deletion of WordPress content/theme/plugin artifacts is allowed only when explicitly requested/approved and rollback exists. Repository deletion remains governed by `github-operations` permanent deny and is unrelated to WordPress content deletion.

## Completion

Return `PASS`, `REVIEW`, `BLOCKED` or `ROLLBACK_REQUIRED` with map reference, change evidence, verification results and remaining risks. Never claim production success from HTTP status alone; verify resulting WordPress state and front-end behavior.
