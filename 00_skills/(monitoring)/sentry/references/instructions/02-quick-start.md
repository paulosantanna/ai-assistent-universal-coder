<!-- Package: 00_skills/(monitoring)/sentry; relative command/resource examples resolve from that package or workspace root. -->

## Quick start

- If not already authenticated, ask the user to provide a valid `SENTRY_AUTH_TOKEN` (read-only scopes such as `project:read`, `event:read`) or to log in and create one before running commands.
- Set `SENTRY_AUTH_TOKEN` as an env var.
- Optional defaults: `SENTRY_ORG`, `SENTRY_PROJECT`, `SENTRY_BASE_URL`.
- Defaults: org/project `{your-org}`/`{your-project}`, time range `24h`, environment `prod`, limit 20 (max 50).
- Always call the Sentry API (no heuristics, no caching).

If the token is missing, give the user these steps:

1. Create a Sentry auth token: <https://sentry.io/settings/account/api/auth-tokens/>
2. Create a token with read-only scopes such as `project:read`, `event:read`, and `org:read`.
3. Set `SENTRY_AUTH_TOKEN` as an environment variable in their system.
4. Offer to guide them through setting the environment variable for their OS/shell if needed.

- Never ask the user to paste the full token in chat. Ask them to set it locally and confirm when ready.
