# AEOS Agents contract

Governance: CodENavi Full Workspace v2

Inherits root `AGENT.md` and `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`.

All agents/subagents in this subtree must operate through **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**.

Each agent contract must preserve:
- bounded responsibility and authority;
- explicit inputs, outputs and handoff state;
- evidence expectations and uncertainty labels;
- stop/escalation conditions;
- registered capabilities only;
- no self-escalation or bypass of Judge/approval/rollback;
- verification before completion;
- notebook/docs/memory update when durable knowledge changes.

Delegation does not transfer unlimited authority. The delegating agent remains responsible for integration and verification.
