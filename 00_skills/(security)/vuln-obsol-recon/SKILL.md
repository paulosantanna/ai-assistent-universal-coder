---
name: vuln-obsol-recon
description: Assess known vulnerabilities and lifecycle risk for the exact versions detected in repository/runtime evidence. Use when the user says esta versão tem CVE, tecnologia está obsoleta or mapear vulnerabilidade e EOL. Do NOT use for base synchronization, patch implementation, deep PR security review or invented versions without manifests/runtime evidence.
license: CC-BY-4.0
metadata:
  author: AEOS; photographic reference supplied by user
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Vuln Obsol Recon

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Assess known vulnerabilities and lifecycle risk for the exact versions detected in repository/runtime evidence.

## Workflow

1. Identify ecosystem, package/product/distribution, exact detected version and provenance (production, repository/lockfile, inherited BOM or unknown).
2. Read [providers](references/providers.md); query available current advisory/lifecycle sources with the exact ecosystem/version, preserving source time and affected-range semantics.
3. Classify vulnerability exposure separately from obsolescence; record severity, fixed release, support/EOL status and evidence for each conclusion.
4. Reconcile contradictory providers without counting duplicate advisories as distinct vulnerabilities; retain unknown when coverage or matching is inconclusive.
5. Write the repository-specific verdict and route refreshes to cve/eol-advisory-sync, and known fixes to cve-remediation.

## Rules

- Do not confuse repository latest with the deployed version. No vulnerability-free claim from a missing scan.
- Community discussion is supporting operational context, not authority for version ranges or lifecycle dates.
- No secret values in evidence; only provider identifiers, timestamps and source pointers.

## Inputs and outputs

Inputs: the user-requested target, authorized source paths/access, scope and expected result.

Separate CVE and EOL findings with exact version/provenance, current sources, freshness, uncertainty and suggested next action.

## Verification and stop

Verify the actual outputs and relevant contract checks. Missing evidence, dependency, source asset, input or permission blocks its dependent stage; report the precise gap.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
