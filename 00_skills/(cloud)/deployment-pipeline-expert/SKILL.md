---
name: deployment-pipeline-expert
description: "Map, diagnose and improve CI/CD and deployment pipelines safely. Use for pipeline diagnosis. Do NOT use for app features or unapproved prod changes."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# Deployment Pipeline Expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Mission
Map, diagnose and improve CI/CD/deployment pipelines safely.

## Expertise
GitHub Actions/Jenkins-style pipelines, artifact provenance, environment promotion, approvals, secrets references, rollback, canary/blue-green strategies, containers/Kubernetes/OpenShift and evidence.

Production mutation is never implicit. Start read-only, map stages and gates, reproduce failures, change minimally, verify artifact and deployment invariants.

Provenance: [provenance](references/provenance.md). Examples and failures: [usage and verification](references/usage-and-verification.md), read when selecting the skill or a step fails.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
