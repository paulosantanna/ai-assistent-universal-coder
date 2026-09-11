# Skill: kinghost-secure-connection

## Mission
Establish governed authenticated sessions to authorized KingHost resources for other AEOS skills without persisting credentials.

## Uses MCP
- kinghost-commerce

## Supported Authentication Inputs
- username + password supplied at execution time
- SSH key reference supplied through an approved secret provider
- short-lived session/token when officially supported
- operator-provided database credentials used only for an opaque runtime session

## Credential Contract
Credentials are runtime inputs, never knowledge. Passwords, tokens and private keys MUST NOT be committed, embedded in skill files, written to evidence, logs, Chromatic memory, prompts, reports or exception messages. Prefer a secret reference/ephemeral injection over plaintext whenever available.

## Allowed Actions
- Resolve the authorized target host/account.
- Validate host identity before authentication.
- Establish FTP/SFTP/SSH/database/control-plane sessions only through the governed MCP adapter.
- Test authentication and minimum required permissions.
- Return an opaque session reference to downstream skills.
- Close/revoke the session after the governed operation.
- Produce an access request plan that names needed fields without collecting secrets when credentials are not yet available.

## Forbidden Actions
- Persist username/password pairs.
- Echo credentials.
- Disable TLS/host-key validation to make a connection work.
- Credential stuffing, brute force or discovery of unknown credentials.
- Cookie extraction, browser session dumping, saved-password scraping or filesystem secret hunting for access.
- Connect to targets not explicitly authorized by the operator.
- Give downstream skills raw secrets when an opaque session handle is sufficient.

## Required Inputs
- target
- protocol
- authorization_context
- credential_reference_or_ephemeral_input

## Output Schema
```json
{"status":"CONNECTED|DENIED|BLOCKED","session_ref":"opaque|null","target_fingerprint":"","capabilities":[],"expires_at":"","evidence_refs":[],"blocking_conditions":[]}
```

## Quality Gates
- Target authorization proven.
- Server identity validation enabled.
- Least-privilege capability set established.
- Secrets redacted from all durable outputs.
- Session has bounded lifetime and explicit close path.

## Stop Conditions
Unauthorized target; invalid host identity; credential would need durable storage; insecure transport; permission scope cannot be bounded.