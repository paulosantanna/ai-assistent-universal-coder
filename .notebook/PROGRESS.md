# PROGRESS

Updated: 2026-09-16

## Active Mission
- Objective: one-command KingHost playbook that publishes a locally altered PHP/WordPress/WooCommerce site onto an already-hosted Hospedagem domain.
- [x] BRIEFING: operator wants a single AI/command path for KingHost WordPress + WooCommerce publish.
- [x] RECON: `kinghost-expert-production-lifecycle` is the general FSM; no one-command playbook or CLI existed.
- [x] PLAN: add `kinghost-wordpress-publish`, `publish.preflight`, `npm run aeos:kinghost:publish`, WooCommerce preserve-live-data policy.
- [x] EXECUTE: playbook, MCP preflight, CLI, overlay, tests, notebook.
- [x] VERIFY: Jest 65/65, guards PASS, control MCP smoke PASS.
- [x] DEBRIEF: draft PR #43 opened.

## Current Phase
- DEBRIEF

## Verification Gates
- [x] `kinghost-wordpress-publish` loads from overlay.
- [x] Preflight detects local WooCommerce tree and never returns secrets.
- [x] CLI DRY_RUN works without FTP; `--apply` requires `AEOS_KINGHOST_APPROVED=true`.
- [x] `--replace-database` is BLOCKED on the one-command path.
- [x] Skill router sends KingHost publish intent to `kinghost-expert`.
- [x] `npm run aeos:verify` PASS (guards + Jest 12 suites / 65 tests).
- [x] `kinghost-control-mcp` `--self-test` PASS.
- [ ] Live KingHost FTP APPLY against a real domain (requires operator cookie/FTP env).

## Factual Log
- 2026-09-16: Master already contains KingHost control MCP from #42 (`3470353a`).
- 2026-09-16: Added playbook `kinghost-wordpress-publish` and CLI `scripts/aeos-kinghost-publish.mjs`.

## Previous Missions
- Repair PR #42 CI and merge KingHost Hospedagem control MCP (`3470353a`).
- Resolve PR #33 conflicts with master and merge kotlin-expert.
- Require Why/Porquê on every open PR; PR #34 merged (`b71c1bb9`); master CI `34789704932` SUCCESS.
