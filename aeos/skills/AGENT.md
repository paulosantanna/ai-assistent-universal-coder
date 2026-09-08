# AEOS Skills contract

Governance: CodENavi Full Workspace v2

Inherits root `AGENT.md` and `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`.

Every legacy, generated and future skill in this subtree follows **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**.

A valid skill must define or inherit:
- mission and non-goals;
- activation/inputs and bounded scope;
- outputs and evidence;
- owner/risk and valid capabilities;
- security/secret boundaries;
- freshness requirements for APIs/frameworks/models/providers;
- verification/evals and failure semantics;
- handoff/debrief behavior.

Skills never grant authority by themselves. Runtime capability/policy/approval checks remain authoritative. A skill that is only declarative must not claim operational execution until wired and verified.

Old skills automatically inherit this contract; new skills must be written directly to this standard.
