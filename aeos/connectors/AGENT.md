# AEOS Connectors contract

Governance: CodENavi Full Workspace v2

Inherits root `AGENT.md` and `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`.

Connector work follows **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**. External systems are accessed only through documented/authorized interfaces, credentials are runtime-only, retries/idempotency/failure semantics are explicit, and mutations are bounded by capability/policy/approval controls. Unsupported provider behavior fails closed.
