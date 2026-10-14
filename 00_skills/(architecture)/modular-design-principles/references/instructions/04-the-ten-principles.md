<!-- Package: 00_skills/(architecture)/modular-design-principles; relative command/resource examples resolve from that package or workspace root. -->

## The ten principles

| # | Principle | Intent |
|---|-----------|--------|
| 1 | **Well-defined boundaries** | A small, stable **public surface**; everything else is internal. Consumers depend on contracts, not internals. |
| 2 | **Composability** | Modules can be used alone or combined without special knowledge of each other’s internals. |
| 3 | **Independence** | No hidden shared mutable state across boundaries; each module should be testable in isolation (with fakes or test doubles at the edges). |
| 4 | **Individual scale** | Resources (compute, storage, rate limits, batch size) can be tuned **per module** where it matters, without rewriting others. |
| 5 | **Explicit communication** | Cross-module interaction uses **documented contracts** (APIs, events, messages, shared types) — not incidental coupling. |
| 6 | **Replaceability** | Dependencies on other modules are expressed through **interfaces or protocols** so implementations can change. |
| 7 | **Deployment independence** | Modules do not assume they share a process, host, or release cadence unless that is an explicit architectural decision. |
| 8 | **State isolation** | Each module **owns** its persistent state and naming; no silent sharing of the same logical data store or ambiguous global names across boundaries. |
| 9 | **Observability** | Each module can be diagnosed on its own: logs, metrics, traces, health — attributable to the unit that emitted them. |
| 10 | **Fail independence** | Failures are **contained** (timeouts, bulkheads, circuit breaking, idempotency) so one module’s outage does not blindly cascade. |

**Principle 8** is often the hardest: ambiguous ownership of data or names is a frequent source of “works until it doesn’t” integration bugs.

For **depth** (rules for agents + abstract examples per principle), load `references/principles.md`.

---
