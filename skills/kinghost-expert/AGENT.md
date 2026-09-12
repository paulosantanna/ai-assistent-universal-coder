# Local AGENT contract — kinghost-expert

This file specializes root `AGENT.md`; it does not define another agent identity.

## Lifecycle

Follow `BRIEFING -> RECON -> PLAN -> EXECUTE -> VERIFY -> DEBRIEF`.

## First actions

- Identify the workspace WordPress/PHP tree and the KingHost environment.
- Open cookie/Playwright panel or wp-admin session through `runtime-auth` when needed.
- Bind FTP/MySQL credentials as opaque refs from env/secret/runtime memory.
- Run the production FSM in order for live publishes.

## Engineering rules

- Prefer WordPress extension points over FTP of core files.
- Keep remote writes inside the approved `wp-content` root.
- Redact all credential material.
- Close FTP/MySQL/auth sessions after VERIFY or ROLLBACK.
