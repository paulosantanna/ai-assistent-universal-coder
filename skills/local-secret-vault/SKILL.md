# Skill: local-secret-vault
Governance: CodENavi v1

## Mission
Read authorized local credential vaults safely and expose only masked metadata or ephemeral secret references to governed tools.

## Security invariants
- Secret values are runtime-only and never persisted to Git, prompt, chat, notebook, memory, evidence, logs or stdout.
- Inspection output is masked.
- A downstream tool receives an opaque/ephemeral reference when possible, not raw credentials.
- Read-only by default; no secret mutation unless an explicit approved secret-management workflow exists.
- Never brute-force, discover or reuse credentials beyond the authorized target.
- Treat accidentally exposed credentials as compromised.

## Supported parsing model
Sectioned local files may be normalized deterministically (for example records delimited by a leading `@label`), but format discovery must never print the contained secret values.

## Output
`{"status":"PASS|BLOCKED","entries":[{"label":"","target":"","secret_ref":"opaque","masked":"***"}],"evidence_refs":[]}`
