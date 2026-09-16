# Local AGENT contract — kinghost-expert

This file specializes root `AGENT.md`; it does not define another agent identity.

## Lifecycle

Follow `BRIEFING -> RECON -> PLAN -> EXECUTE -> VERIFY -> DEBRIEF`.

## First actions

- Identify the workspace WordPress/PHP tree and the KingHost environment.
- Open the panel cookie jar with `kinghost_control.panel.session.open_cookie_file`.
- List and select an existing hosting domain.
- Bind FTP/MySQL credentials as opaque refs from env/secret/runtime memory.
- Clone the remote site when the local tree is missing, then run the production FSM for live publishes.

## Engineering rules

- Prefer WordPress extension points over FTP of core files.
- Keep remote writes inside the approved `wp-content` root.
- Redact all credential material.
- Close FTP/MySQL/auth sessions after VERIFY or ROLLBACK.
