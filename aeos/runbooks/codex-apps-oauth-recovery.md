# Codex Apps OAuth Recovery

Use this runbook when startup logs show `codex_apps` failing with `HTTP 401` and `token_revoked`.

## Classification

- Status: external authentication blocked.
- Runtime behavior: fail soft for optional external connectors.
- Secret handling: never extract cookies, browser storage, OAuth tokens, or passwords.
- Repository policy: never persist recovered credentials in git, config files, evidence, or logs.

## Recovery

1. Reconnect the affected app/account in the approved Codex or ChatGPT connector UI.
2. Run:

   ```bash
   npm run aeos:guard:codex-apps-oauth -- --log-file <startup-log>
   ```

3. Run the MCP health check again after reconnecting.

## Expected Guard Output

For revoked auth, the guard returns `blocked_external_auth`, `fail_soft: true`, and remediation steps. This means the workspace can keep loading local skills and local MCP servers while the external connector waits for an operator reconnection.