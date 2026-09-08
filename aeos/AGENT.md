# AEOS subtree contract

Governance: CodENavi Full Workspace v2

This subtree inherits the root `AGENT.md` and `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`.

Every AEOS artifact under this directory — agents, skills, playbooks, MCPs, LCPs, registries, blueprints, config/policies, evals, knowledge, memory, evidence contracts and runtime-facing metadata — follows **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**.

Rules:
- evidence before claims;
- current repository/provider/framework evidence before memory;
- observed/inferred/unknown must remain distinct;
- surgical changes only;
- capabilities and policies are deny-by-default boundaries;
- no secret persistence;
- high-impact changes require existing approval/Judge/rollback gates;
- stale artifacts are updated or deprecated in the same mission;
- a declarative contract is not considered operational unless runtime wiring exists and is verified.

Nearest local `AGENT.md` files may specialize this contract but never weaken root governance.
