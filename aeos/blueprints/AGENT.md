# AEOS Blueprints contract

Governance: CodENavi Full Workspace v2

Inherits root `AGENT.md` and `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`.

All blueprints follow **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**.

Blueprints must:
- separate current state from target state;
- mark relationships/components as observed, inferred or unknown;
- map trust boundaries, data ownership, failure propagation and operational constraints;
- expose trade-offs and rejected alternatives for durable decisions;
- use ADRs when a choice materially constrains future architecture;
- avoid diagrams that merely mirror folders without runtime/dependency evidence;
- include migration/verification/rollback implications for target-state changes.

Legacy blueprints inherit this contract automatically.
