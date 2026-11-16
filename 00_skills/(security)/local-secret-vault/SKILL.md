---
name: local-secret-vault
description: "Read authorized local credential vaults, exposing only masked metadata. Use for local vault access. Do NOT use outside scope or to expose secrets."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Skill: local-secret-vault

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

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

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

Read [photographed sectioned-vault rules](../../../01_siglas/_comum/ferramentas/cofre-cookier.md) only for an explicitly authorized external sectioned vault. Normalize CRLF/CR, preserve the full label and validate format in runtime; never evaluate a shell command from a vault or print a section body. Paths in photos are examples, not authorized providers.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
