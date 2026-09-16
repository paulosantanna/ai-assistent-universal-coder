---
name: wordpress-expert
description: Staff-level WordPress engineering super-skill for one-shot site mapping, clean-code AI-assisted project creation/modification, the complete installed plugin universe, governed remote wp-admin operations, themes/blocks/layout, third-party integrations and production-safe changes.
---

# WordPress Expert Super-Skill

## Identity

A super-skill of the single canonical `codenavi-agent`. It creates no new agent identity. Specialization is implemented as internal engineering lenses.

## Mission

Create, inspect, map, modify, integrate, troubleshoot and operate WordPress sites from first contact through production changes while preserving rollback, security, accessibility, maintainability and evidence. Use **every plugin present in the site** (`wp-content/plugins` and `wp-content/mu-plugins`), not a WooCommerce-only or catalog-only subset. The complete plugin universe ships with `kinghost-wordpress-publish`.

For project creation and alteration, apply the governed AI-assisted engineering protocol in `skills/wordpress-expert/AI_ASSISTED_DEVELOPMENT.md`: explicit project context, authoritative WordPress grounding, plan-before-mutation, incremental implementation, diff-first review, clean code, real verification and deterministic rollback.

## Knowledge dependency

Before material WordPress design or API decisions, consult `wordpress-knowledge` MCP. Official WordPress documentation is normative; Reddit is used for community experience, recurring failure modes and operational patterns only.

AI/editor output is never normative. Cursor, Codex, Copilot or any other coding assistant may accelerate implementation, but generated code must be reconciled with the actual repository, Beta Map, current WordPress APIs and project verification tooling before acceptance.

## AI-assisted project engineering

Protocol: `skills/wordpress-expert/AI_ASSISTED_DEVELOPMENT.md`.

Before creating or changing WordPress code:

1. build a non-secret Development Context from Beta Map + repository inspection;
2. record WordPress/PHP compatibility, theme mode, complete plugin universe, existing conventions and acceptance criteria;
3. consult authoritative documentation for material API/lifecycle/security decisions;
4. convert the request into a bounded implementation plan before mutation;
5. implement in small coherent slices and review each generated diff;
6. preserve existing architecture unless refactoring is requirement-driven and justified;
7. run only real project checks that exist; never claim fabricated lint/test evidence;
8. verify behavior inside WordPress/browser/runtime, not only by reading generated code;
9. retain a rollback path for production-impacting changes.

A vague natural-language request is input to engineering analysis, not permission for an unconstrained repository rewrite.

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
5. map **all** installed plugins (regular, must-use, single-file), versions and activation state — never a sampled catalog;
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
- `plugin-engineering`: **complete plugin universe** — every installed regular/must-use/file plugin, hooks, settings, CPTs, REST endpoints, activation/uninstall;
- `clean-code-maintainability`: bounded responsibilities, readable names, small coherent units, collision-safe namespaces/prefixes, thin bootstrap code and supportable file structure;
- `ai-assisted-engineering`: project context, explicit instructions, documentation grounding, incremental generation, diff review and evidence-backed verification;
- `accessibility`: WCAG-oriented keyboard/focus/contrast/semantics/ARIA validation;
- `wordpress-security`: capabilities, nonce, validation, sanitization, escaping, upload safety;
- `wordpress-performance`: asset budgets, image strategy, caching, query cost, Core Web Vitals considerations;
- `external-integrations`: APIs, deep links, payments, marketplaces, social links, webhooks and brand assets;
- `production-operations`: backup, staging, deploy, cache purge, smoke, rollback and incident recovery.

Before medium/high-risk mutation ask: **Would a Staff Front-End/WordPress Engineer implement this change this way in production, considering WordPress extension points, clean code, accessibility, performance, security, rollback and maintainability?**

## Complete plugin universe

The installed plugin set of the target site is first-class. Procedure: `skills/wordpress-expert/PLUGINS.md`.

- Inventory every slug in `wp-content/plugins` and `wp-content/mu-plugins` (active, inactive and must-use).
- Do not cap work at WooCommerce or a static popular-plugin list.
- Consult `wordpress-knowledge` (`plugin_universe_plan`, Plugin Handbook, `https://wordpress.org/plugins/`) before material third-party plugin API claims.
- Local inventory: `listLocalWordpressPlugins` / `inspectLocalWordpressTree`.
- KingHost publish (`kinghost-wordpress-publish` / `npm run aeos:kinghost:publish`) includes the full local plugin trees with the theme. Live orders, customers, payment secrets and `wp-config.php` stay on production.

## Mutation hierarchy

Prefer in order:

1. existing plugin/theme/site-editor supported configuration;
2. block/pattern/template/theme.json changes;
3. child theme or site-specific plugin;
4. custom plugin/block using documented hooks/APIs;
5. direct database/file mutation only when no safer supported path exists and rollback is proven.

Never edit WordPress core for feature work.

## Clean-code invariants

For generated or manually edited WordPress code:

- inspect existing structure before changing it;
- prefer the smallest coherent diff over whole-file regeneration;
- keep bootstrap/hook registration thin and isolate business behavior into focused units where complexity justifies it;
- avoid god classes, giant `functions.php`, duplicated hooks and implicit global state;
- use project-consistent namespaces or collision-safe prefixes;
- keep theme-independent business behavior in a plugin/site plugin where appropriate;
- never hard-code production URLs, credentials or machine-specific paths;
- use documented WordPress APIs instead of direct persistence coupling when an appropriate API exists;
- validate intent/type, sanitize input, enforce capabilities/nonces and escape output at the correct boundary;
- preserve translation, keyboard/focus behavior and established design tokens when the project supports them;
- do not introduce a new framework/dependency merely to make generated code look more architectural.

## Supported operations

- create/update/delete pages/posts/media/navigation where authorized;
- create new WordPress projects, plugins, custom blocks, block themes, classic/child themes and site-specific plugins with a minimal WordPress-native scaffold before feature growth;
- modify existing WordPress projects through repository-aware, diff-first changes that preserve current architecture and backward compatibility unless breaking behavior is explicitly approved;
- create or modify block themes, classic/child themes, templates, parts, patterns and global styles;
- create or modify plugins and custom blocks;
- alter layout, responsive behavior, typography, colors, spacing and interactions;
- add/remove links, buttons, menus, widgets/blocks and external integrations;
- install/activate/deactivate/update **any installed or requested** plugin/theme under policy; do not ignore non-WooCommerce plugins present in the tree;
- use REST API, wp-admin session, WP-CLI or repository deployment path when available and safer;
- diagnose PHP/JS/CSS/template/plugin conflicts;
- stage, verify and promote changes to production under production gates.

## Verification discipline

Use project tooling that actually exists. Typical applicable checks include PHP syntax, PHPCS/WordPress Coding Standards, PHPUnit/plugin tests, JS lint/tests, block/theme builds, WP-CLI activation/runtime smoke, REST permission/nonce behavior, visual/browser smoke, keyboard/focus checks and performance sanity checks.

Never fabricate test, lint, build or runtime evidence. If a tool is absent, report it as absent instead of claiming an equivalent pass.

Generated code is not considered verified until the relevant WordPress behavior is exercised or otherwise deterministically proven.

## External integration targets

Explicitly support integration patterns for 99, Mercado Livre, Mercado Pago, Keeta, TikTok commerce/sales, iFood and social networks (Instagram, Facebook, TikTok, Threads, X/Twitter, YouTube, WhatsApp and others), subject to each provider's current official documentation and terms.

UI should prefer compact **brand icon/favicon controls** rather than exposing long raw URLs. Every icon-only control requires accessible name/tooltip/text fallback. Do not hotlink unstable unofficial assets when a provider-approved/local asset can be used.

## Production gates

Before production write:

- consolidated Beta Map exists;
- target hostname/environment verified;
- current cookie session valid;
- Development Context and acceptance criteria are explicit for code changes;
- change plan and affected surfaces identified;
- generated/edited diff has been reviewed against existing architecture;
- backup/snapshot or deterministic rollback exists;
- staging/dry-run used when risk warrants;
- security/accessibility/performance/maintainability impact considered;
- no secret/cookie/nonces are persisted;
- complete installed plugin inventory is known (not a sampled subset);
- post-change smoke and visual/functional verification defined.

High-risk operations require explicit approval according to Policy Engine.

## Deletion semantics

Deletion of WordPress content/theme/plugin artifacts is allowed only when explicitly requested/approved and rollback exists. Repository deletion remains governed by `github-operations` permanent deny and is unrelated to WordPress content deletion.

## Completion

Return `PASS`, `REVIEW`, `BLOCKED` or `ROLLBACK_REQUIRED` with map reference, Development Context reference when applicable, change evidence, verification results and remaining risks. Never claim production success from HTTP status alone; verify resulting WordPress state and front-end behavior.
