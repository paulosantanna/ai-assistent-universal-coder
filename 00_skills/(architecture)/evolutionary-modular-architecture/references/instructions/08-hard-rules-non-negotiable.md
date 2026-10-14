<!-- Package: 00_skills/(architecture)/evolutionary-modular-architecture; relative command/resource examples resolve from that package or workspace root. -->

## Hard rules (non-negotiable)

- Each module **writes only its own tables**; cross-context links are by id, validated in code (`enforce-module-boundaries`).
- **No direct cross-module imports** — communicate via facade/contract or event.
- **Every external system sits behind a port + ACL** — no vendor model leaks into the domain.
- **Retry only idempotent operations**; writes carry an idempotency key.
- **Modular principles (P1–P10) beat structural ones (P11–P19).** If co-locating would force a cross-module entity import, use a facade + DTO; if splitting an aggregate would break a transaction, keep it together.

---
