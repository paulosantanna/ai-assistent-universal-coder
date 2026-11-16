---
name: fable-domain
description: "Research a domain and build a Fable adapter, flowchart, trap fixture and smoke eval. Use for new sector adapters. Do NOT use for unrelated stacks."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Enterprise Skill: fable-domain

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

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

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
