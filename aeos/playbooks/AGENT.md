# AEOS Playbooks contract

Governance: CodENavi Full Workspace v2

Inherits root `AGENT.md` and `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`.

Every playbook in this subtree must map its behavior to **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**.

Requirements:
- preconditions and acceptance criteria before execution;
- explicit dependency/order semantics;
- smallest sufficient plan;
- every mutation has verification and failure handling;
- risky/production mutations define rollback or compensation;
- parallel steps only when dependency-safe;
- capabilities are bounded by registered skills/MCPs/LCPs/tools;
- no secret persistence or credential echo;
- evidence and terminal/handoff state are mandatory;
- documentation/notebook impact is evaluated before completion.

Legacy playbooks inherit this contract automatically and may not weaken it.
