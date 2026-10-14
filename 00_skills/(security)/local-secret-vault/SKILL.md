---
name: local-secret-vault
description: Read authorized local credential vaults safely and expose only masked metadata or ephemeral secret references to governed tools. Use when the user requests local secret vault or invokes local-secret-vault. Do NOT use outside authorized defensive scope or to expose secret values.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: local-secret-vault

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

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

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.

Read [photographed sectioned-vault rules](../../../01_siglas/_comum/ferramentas/cofre-cookier.md) only for an explicitly authorized external sectioned vault. Normalize CRLF/CR, preserve the full label and validate format in runtime; never evaluate a shell command from a vault or print a section body. Paths in photos are examples, not authorized providers.
