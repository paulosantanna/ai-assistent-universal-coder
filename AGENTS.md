# AGENTS.md
# AEOS compatibility entry point

`AGENT.md` is the canonical root constitution. This file exists because external agents/tools may search specifically for `AGENTS.md`.

Every consumer of this file MUST immediately load, in order:

1. `AGENT.md`
2. `references/CODENAVI_WORKSPACE_STANDARD.md`
3. `.notebook/INDEX.md` when present
4. the selected skill/playbook/MCP/LCP contract

The mandatory mission lifecycle is **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**.

No agent may weaken the canonical rules by relying on an older local copy. If `AGENT.md` and `AGENTS.md` diverge, `AGENT.md` wins and the divergence is a governance defect that must be corrected.

Secrets are runtime-only, masked and non-persistent. Technical terms remain in their canonical nomenclature. Knowledge is verified against current evidence and stale notes are updated or deprecated in the same mission.
