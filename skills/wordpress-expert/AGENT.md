# Local AGENT contract — wordpress-expert

This file specializes root `AGENT.md`; it does not define another agent identity.

## Lifecycle

Follow `BRIEFING -> RECON -> PLAN -> EXECUTE -> VERIFY -> DEBRIEF`.

## First contact

- Resolve canonical base URL and derive site_id.
- Use external runtime cookie/cookie-jar reference for wp-admin authentication.
- If no consolidated Beta Map exists, run read-only mapping first and do not combine first mapping with unrelated production mutation unless explicitly authorized as an emergency.
- Once consolidated, never repeat full mapping automatically; later runs perform delta/preflight only.

## AI-assisted development contract

For WordPress project creation or modification, follow `skills/wordpress-expert/AI_ASSISTED_DEVELOPMENT.md`.

Before editing code:

- construct a non-secret Development Context from repository state plus Beta Map;
- identify WordPress/PHP compatibility, theme mode, complete plugin universe, existing conventions and acceptance criteria;
- consult `wordpress-knowledge` for material WordPress API/lifecycle/security decisions;
- produce a bounded implementation sequence before mutation;
- prefer incremental, reviewable diffs to large regenerated files;
- verify generated code with the real project/runtime tooling that exists;
- do not treat output from Cursor, Codex, Copilot or another assistant as authoritative evidence.

## Engineering rules

- Prefer WordPress extension points over core edits.
- Use every plugin present in `wp-content/plugins` and `wp-content/mu-plugins`; do not reduce the site to WooCommerce or a static catalog.
- Respect block vs classic theme architecture.
- Separate content, presentation and business integration concerns.
- Keep bootstrap/hook registration focused; avoid giant `functions.php`, god classes, duplicated hooks and accidental global state.
- Use project-consistent namespaces or collision-safe prefixes and descriptive names.
- Preserve the existing architecture unless a requirement-driven refactor is explicitly justified.
- Never hard-code production URLs, secrets or machine-specific paths.
- Sanitize input, validate intent/type, check capabilities, use nonce/CSRF protection and escape output.
- Preserve accessibility for icon-only external service controls and generated UI.
- Treat third-party API/deep-link behavior as current external knowledge; verify official provider docs before production.
- For production changes, require rollback and post-change verification.
- Never claim lint/test/build/runtime success unless the check was actually executed.

## Cookie rule

The cookie file itself may be read and used at runtime. Raw cookie values may not be copied into workspace artifacts or model context. Cookie-path/reference metadata may be passed only to the governed runtime adapter and may be recorded as a provider alias, not raw contents.
