<!-- Package: 00_skills/(architecture)/evolutionary-modular-architecture; relative command/resource examples resolve from that package or workspace root. -->

## Reference guide

| Load this file | When |
| --- | --- |
| `references/principles.md` | You need the exact principle text, or to resolve a structural-vs-modular conflict. |
| `references/ddd.md` | Phase 1–2: classifying subdomains, drawing the context map, deciding tactical intensity. |
| `references/flat-by-aggregate.md` | Phase 3: laying out a module; flat vs subdomain; scaffolding; facades; tests. |
| `references/acl-and-communication.md` | Phase 4: ports/adapters/ACL, events + outbox, SSE. |
| `references/resilience.md` | Phase 5: backoff/jitter, circuit breaker, idempotency, bulkhead, durable execution. |
| `references/stack-2026.md` | Phase 0/6: concrete stack choices and trade-offs. |
| `references/architecture-doc.md` + `assets/architecture-template.html` | Phase 7: producing the HTML architecture document and its diagrams. |
| `scripts/validate-structure.mjs`, `scripts/validate-boundaries.mjs` | Validation: enforcing structure and module boundaries in CI or before merge. |
