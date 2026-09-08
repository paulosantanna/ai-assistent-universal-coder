# KingHost Commerce MCP adapter contract

Governance: CodENavi Full Workspace v2

Inherits root `AGENT.md` and `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`.

All adapter operations follow **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**.

Specific rules:
- authenticated sessions are ephemeral and secrets are runtime-only;
- host identity is verified; trust-on-first-use requires explicit operator intent;
- read-only is the default posture;
- filesystem/database mutations require bounded scope, approval/change tracking and rollback reference where defined;
- no arbitrary shell; command/action allowlists fail closed;
- remote paths and database queries must remain scoped and validated;
- provider capabilities are verified against current official KingHost evidence before high-impact actions;
- errors/evidence redact credentials and sensitive values;
- declarative actions not implemented by the adapter must return unsupported, never simulated success;
- adapter changes require smoke/integration/security regression checks.
