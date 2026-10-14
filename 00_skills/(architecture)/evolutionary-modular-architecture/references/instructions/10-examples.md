<!-- Package: 00_skills/(architecture)/evolutionary-modular-architecture; relative command/resource examples resolve from that package or workspace root. -->

## Examples

### Example 1: Design a new platform

User says: "Desenhe a arquitetura de uma plataforma de contas a pagar que lança no ERP do cliente."
Actions:
1. Phase 1 — discover subdomains; classify (e.g., Payables and Operations as Core; Documents/Audit/Gamification as Supporting; Identity/Notifications as Generic).
2. Phase 2 — context map + one-database, table-per-module ownership.
3. Phase 3 — flat-by-aggregate layout per module.
4. Phase 4 — ERP/ticketing/storage behind ports + ACL; events via outbox; SSE for the operator queue.
5. Phase 5 — resilience policy on the ERP adapter (idempotency key = payment id).
6. Phase 6 — 2026 stack + evolution note (one deploy now).
Result: a context map, module layouts, a port/adapter list, a resilience policy, and a stack + evolution plan — each grounded in the matching reference.

### Example 2: Organize a module

User says: "Como organizo o módulo de billing?"
Actions: read `references/flat-by-aggregate.md`; propose `billing/subscription/`, `billing/invoice/`, `billing/payment/` with co-located files and `__test__/`; run the 6-criteria test (billing = flat). Result: a flat folder tree with rationale and the dependency rule preserved via suffixes.

### Example 3: Decouple from a vendor

User says: "Não quero ficar preso ao OMIE."
Actions: read `references/acl-and-communication.md`; define `ErpLedgerPort` in domain language; implement `OmieAdapter`; translate the OMIE model at the boundary; show that swapping ERPs means swapping the adapter. Result: a port interface + adapter plan; the domain never imports vendor types.

---
