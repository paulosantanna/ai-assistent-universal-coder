<!-- Package: 00_skills/(architecture)/evolutionary-modular-architecture; relative command/resource examples resolve from that package or workspace root. -->

## Core model (load the matching reference when you go deep)

| Topic | What it covers | Reference |
| --- | --- | --- |
| Principles | 10 modular (P1–P10) + 9 structural (P11–P19) + conflict hierarchy | `references/principles.md` |
| DDD | Strategic (subdomains, context map, integration patterns) + tactical (rich aggregates, intensity by subdomain) | `references/ddd.md` |
| Module internals | Flat-by-aggregate, suffixes, depth, flat vs subdomain test, scaffolding | `references/flat-by-aggregate.md` |
| Communication | Ports & Adapters / ACL, events + transactional outbox, SSE real-time | `references/acl-and-communication.md` |
| Resilience | Backoff + full jitter, circuit breaker, retry budget, idempotency, bulkhead, timeouts | `references/resilience.md` |
| Stack 2026 | Frontend, backend, data, observability, durable workflow, decisions | `references/stack-2026.md` |
| Architecture doc | Building the elegant, self-contained HTML architecture document with SVG diagrams | `references/architecture-doc.md` + `assets/architecture-template.html` |
| Validation | Deterministic checks for structure and module boundaries | `scripts/validate-structure.mjs`, `scripts/validate-boundaries.mjs` |

Do not load all references at once. Read a reference only when the current phase needs it (the workflow below states when).

---
