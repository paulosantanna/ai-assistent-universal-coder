---
name: javascript-expert
description: Implement, diagnose and modernize JavaScript projects with exact runtime/module-system/browser compatibility and repository-native patterns. Use when the user requests javascript expert or invokes javascript-expert. Do NOT use for unrelated languages, domains or production deployment.
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 1.0.0
  owner_agent: codenavi-agent
---

# JavaScript Expert

Governance: CodENavi Full Workspace v2. Skill of `codenavi-agent`; inherit `AGENTS.md`.
Lifecycle: BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF.
Source roles/workers are internal lenses. Never create agent identities or bypass runtime secret/permission gates.

Governance: CodENavi Full Workspace v2

## Mission
Implement, diagnose and modernize JavaScript projects with exact runtime/module-system/browser compatibility and repository-native patterns.

## Recon
Detect Node/browser targets, package manager+lockfile, ESM/CJS boundary, bundler/transpiler, framework and test/lint config. Use `docs-javascript-current` and `docs-node-current` for uncertain API/runtime behavior.

## Execute
Preserve module/import style, async/error patterns and project conventions. Avoid implicit runtime upgrades and unnecessary dependencies. Treat browser and server trust boundaries separately.

## Verify
Lint/type checks if configured, unit/integration/e2e, runtime/module resolution, browser compatibility and security/performance where affected.

## Token discipline
Read `references/INDEX.md`; select runtime/module/verification reference only as required.

Provenance and source freshness: [provenance](references/provenance.md).

Example usage and failure handling: read [usage and verification](references/usage-and-verification.md) when selecting this skill or a required step fails.
Read [runtime-modules.md](references/runtime-modules.md) only when the domain workflow needs that supporting context; root governance and this entry take precedence.
