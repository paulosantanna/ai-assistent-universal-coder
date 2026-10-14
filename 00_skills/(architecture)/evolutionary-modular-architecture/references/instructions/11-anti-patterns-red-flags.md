<!-- Package: 00_skills/(architecture)/evolutionary-modular-architecture; relative command/resource examples resolve from that package or workspace root. -->

## Anti-patterns / red flags

- ❌ Microservices or many databases from day one ("it feels big" is not a reason).
- ❌ Technical-layer folders (`core/service/`, `http/controller/`, `persistence/entity/`) inside a module — that is the legacy pattern flat-by-aggregate replaces.
- ❌ A module reading or writing another module's tables.
- ❌ Vendor SDK types leaking into the domain (no ACL).
- ❌ Retrying non-idempotent writes; retries without backoff + jitter; retries with no budget.
- ❌ Splitting a cohesive transactional Core into event-coupled fragments.
- ❌ Forcing rich tactical DDD on a Generic subdomain that has no invariants.
