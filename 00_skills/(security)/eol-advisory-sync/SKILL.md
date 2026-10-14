---
name: eol-advisory-sync
description: Refresh local end-of-life/support metadata from endoflife.date API v1 and official maintainers with product aliases and freshness. Use when the user says atualizar a base EOL or sincronizar obsolescência. Do NOT use for CVE synchronization, vulnerability patching, or claiming unsupported internal libraries have public EOL dates.
license: CC-BY-4.0
metadata:
  author: AEOS; photographic reference supplied by user
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Eol Advisory Sync

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Refresh local end-of-life/support metadata from endoflife.date API v1 and official maintainers with product aliases and freshness.

## Workflow

1. Inspect existing product aliases, snapshot freshness and the configured API v1 synchronizer.
2. Fetch the declared product/release scope through authorized HTTP access; preserve source dates and distinguish EOL from extended/commercial support.
3. Map aliases to concrete products/distributions; Java requires the actual distribution rather than an invented aggregate Java record.
4. Validate dates, source URLs, schema and coverage before atomically replacing the snapshot.
5. Report stale/unavailable products and the exact refresh result; retain the previous valid snapshot if fetching or validation fails.

## Rules

- Internal/private libraries without public lifecycle evidence are unknown, never assigned fabricated EOL dates.
- Do not bypass execution policy, EDR, TLS or proxy controls. A blocked download is reported with a supported recovery option.
- Synchronization supplies evidence; vuln-obsol-recon owns repository-specific assessment.

## Inputs and outputs

Inputs: the user-requested target, authorized source paths/access, scope and expected result.

A dated, hashed EOL snapshot with explicit aliases, product/distribution provenance, coverage and unknown records.

## Verification and stop

Verify the actual outputs and relevant contract checks. Missing evidence, dependency, source asset, input or permission blocks its dependent stage; report the precise gap.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
