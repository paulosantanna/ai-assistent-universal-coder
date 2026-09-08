# AGENTS.md
# AEOS compatibility entry point — CodENavi Full Workspace v2

Governance: CodENavi Full Workspace v2

`AGENT.md` is the canonical root constitution. This file exists because external agents/tools may search specifically for `AGENTS.md`.

Every consumer of this file MUST immediately load, in order:

1. `AGENT.md`
2. `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`
3. `references/CODENAVI_WORKSPACE_STANDARD.md`
4. `.notebook/INDEX.md` when present
5. the nearest local `AGENT.md`
6. the selected skill/playbook/MCP/LCP/LSP/tool/runtime contract

The mandatory mission lifecycle is **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**.

This applies to the entire workspace: agents, subagents, legacy and new skills, playbooks, MCPs, LCPs, LSP/language-server components, tools/adapters, registries, overlays, policies, permissions, blueprints, evals, memory/knowledge, runtime and CI/CD.

No agent or local contract may weaken the canonical rules by relying on an older copy. If root/local contracts diverge, the stricter rule wins and the divergence must be corrected.

Secrets are runtime-only, masked and non-persistent. Technical terms remain in canonical nomenclature. Knowledge is verified against current evidence and stale notes/docs are updated or deprecated in the same mission.
