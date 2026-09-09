# AEOS Workspace Memory

Status: `CURRENT`
Updated: `2026-09-09`

This file contains only current, reusable workspace state. Historical implementation evidence belongs to Git history and CI artifacts, not to an always-loaded memory contract.

## Authority order

1. `AGENT.md`
2. `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`
3. `references/CODENAVI_WORKSPACE_STANDARD.md`
4. `.notebook/INDEX.md`
5. selected skill/playbook/MCP/LCP contracts
6. repository code and current official documentation

## Runtime model

- Canonical identity: `codenavi-agent`.
- Exactly one agent identity is registered.
- Specialization is provided by skills, playbooks, MCPs, LCPs, tools, adapters and critical-thinking lenses.
- Judge is an independent deterministic runtime gate/service.
- Active AEOS orchestration is Node.js/TypeScript.
- Registry and runtime access are fail-closed.
- Evidence, policy, permissions, approval and rollback requirements remain mandatory where applicable.
- Secrets are runtime-only and must be redacted from prompts, logs, reports, evidence and repository files.

## Mission lifecycle

`BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF`

Material work must inspect `.notebook/INDEX.md`, establish evidence before claims, prefer surgical changes and verify completion with deterministic checks when available.

## Knowledge policy

Keep current project intelligence in `.notebook/`. Store concise facts and pointers rather than copied source. Repair stale notes immediately. Do not preserve retired runtime architecture in active memory files; use Git history when historical investigation is explicitly required.

## Verification entry points

- `npm run aeos:guard:single-agent`
- `npm run aeos:verify`
- `npm run aeos:verify:full`

A green guard is necessary but not sufficient: runtime build/tests and applicable integration smoke checks must also pass before production-readiness claims.
