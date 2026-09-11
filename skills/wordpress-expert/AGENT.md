# Local AGENT contract — wordpress-expert

This file specializes root `AGENT.md`; it does not define another agent identity.

## Lifecycle

Follow `BRIEFING -> RECON -> PLAN -> EXECUTE -> VERIFY -> DEBRIEF`.

## First contact

- Resolve canonical base URL and derive site_id.
- Use external runtime cookie/cookie-jar reference for wp-admin authentication.
- If no consolidated Beta Map exists, run read-only mapping first and do not combine first mapping with unrelated production mutation unless explicitly authorized as an emergency.
- Once consolidated, never repeat full mapping automatically; later runs perform delta/preflight only.

## Engineering rules

- Prefer WordPress extension points over core edits.
- Respect block vs classic theme architecture.
- Separate content, presentation and business integration concerns.
- Sanitize input, validate intent, check capabilities, use nonce/CSRF protection and escape output.
- Preserve accessibility for icon-only external service controls.
- Treat third-party API/deep-link behavior as current external knowledge; verify official provider docs before production.
- For production changes, require rollback and post-change verification.

## Cookie rule

The cookie file itself may be read and used at runtime. Raw cookie values may not be copied into workspace artifacts or model context. Cookie-path/reference metadata may be passed only to the governed runtime adapter and may be recorded as a provider alias, not raw contents.
