---
name: fable-domain
description: Research a domain, create a domain adapter, flowchart, trap fixture, and smoke eval for the Fable Method. Use when creating new sector adapters. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Enterprise Skill: fable-domain

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

## Mission

Provide enterprise-grade domain adapter generation capability for the Fable Method inside AEOS v1.1.

## Allowed Actions

- Read authorized workspace files and configuration.
- Perform web research to fetch primary sources for regulations, policies, and domain standards.
- Generate domain adapter bundles under `fable/references/domains/`.

## Forbidden Actions

- Generating adapters for prohibited red-line domains (medical/clinical diagnosis, legal advice, specific buy/sell financial advice).
- Fabricating citations or using memory without fetching primary sources.
- Bypassing human sign-off on domain boundaries.

---

# Domain Adapter Generation Protocol

Follow the four-stage domain bundle generation protocol:
1. **Stage 1 - Discuss & Red-lines Check:** Verify non-red-line domain and genuine difference from coding default.
2. **Stage 2 - Research:** Fetch primary sources for evidence, authority, and regulations.
3. **Stage 3 - Generate Bundle:** Write workflow + mermaid flowchart, adapter matching `TEMPLATE.md`, and trap fixture.
4. **Stage 4 - Verify & Report:** Run mechanical checks, smoke eval, judge pass, and outcome-first report.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
