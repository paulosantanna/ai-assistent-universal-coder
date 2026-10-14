<!-- Package: 00_skills/(architecture)/modular-design-principles; relative command/resource examples resolve from that package or workspace root. -->

## Typical violations (stated abstractly)

1. **Colliding concepts** — the same name or schema for different things in different modules, or duplicate “global” definitions that diverge over time.
2. **Reach-through persistence** — one module reading or writing another module’s tables, buckets, or documents **without** going through an agreed contract.
3. **Centralized data ownership** — a single persistence layer that registers and exposes **all** stores for **all** modules, encouraging hidden coupling.
4. **Logic at the edge** — business rules in transport adapters (HTTP handlers, UI, CLI) instead of domain/application code.
5. **Edge talking to storage directly** — adapters depending on low-level persistence APIs instead of use cases or application services.
6. **Unscoped transactions** — writes that span boundaries without clear transaction ownership and failure semantics.
7. **Leaky exports** — repositories, internal services, or implementation types exposed as the module’s public API.
8. **Facades that aren’t thin** — “public” entry points that embed querying, mapping, or policy instead of delegating to the right layer inside the module.

---
