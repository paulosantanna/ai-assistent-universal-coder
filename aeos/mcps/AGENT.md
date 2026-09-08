# AEOS MCP contract

Governance: CodENavi Full Workspace v2

Inherits root `AGENT.md` and `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`.

All MCPs/tools/provider adapters in this subtree follow **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**.

Mandatory properties:
- explicit transport, tool surface and capability boundary;
- fail-closed behavior for unknown/unsupported actions;
- read-only by default unless mutation is explicitly governed;
- runtime-only secrets and redacted errors/evidence;
- bounded time/output/resource use;
- provider/API behavior verified against current authoritative documentation;
- no reliance on private/undocumented APIs unless explicitly authorized and evidenced;
- production mutations require approval/Judge/change tracking/rollback where applicable;
- declarative tools are not advertised as executable until runtime wiring and tests prove execution.

Existing MCP files inherit this contract even when their local schema predates CodENavi.
