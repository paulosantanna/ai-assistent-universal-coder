<!-- Package: 00_skills/(development)/nestjs-modular-monolith; relative command/resource examples resolve from that package or workspace root. -->

## Core Workflow

### Phase 1: Discovery

Before writing any code, understand the domain.

1. **Identify the business domain** — What problem does the system solve?
2. **Map bounded contexts** — Which business capabilities are distinct?
3. **Define aggregates and entities** — What are the core domain objects?
4. **Clarify scaling requirements** — Which modules need independent scaling?
5. **Identify integrations** — External systems, APIs, event sources?

**Ask the user about stack preferences:**

- HTTP adapter: Fastify (recommended for performance) or Express?
- ORM: Prisma (type-safe, recommended) or TypeORM?
- API style: tRPC (type-safe) or REST with Swagger?
- Monorepo: NX (recommended) or Turborepo?
- Linting: Biome (fast, recommended) or ESLint+Prettier?
- Auth: Passport/JWT or Better Auth? (see `references/authentication.md`)
- Complexity: Simple services (default) or CQRS? (see `references/architecture-patterns.md`)

**Exit criteria:**

- [ ] Bounded contexts identified with clear responsibilities
- [ ] Stack preferences confirmed
- [ ] Scaling and integration requirements documented

### Phase 2: Design

Architect the system before implementation.

1. **Design module structure** — Map bounded contexts to NX libraries
2. **Define module interfaces** — Public API surface of each module
3. **Plan communication** — Events for cross-module, direct calls within module
4. **Design data model** — Per-module schemas with state isolation
5. **Plan authentication** — Choose and configure auth strategy

Load `references/architecture-patterns.md` for Clean Architecture layers and module structure guidance.

**Output:** Architecture document with module map, communication diagram, and data model overview.

**Exit criteria:**

- [ ] Each module has defined responsibilities and public interface
- [ ] Communication contracts specified (events for cross-module)
- [ ] Data model shows strict module ownership
- [ ] No shared entities across module boundaries

### Phase 3: Implementation

Build modules following Clean Architecture layers. For each module, implement in this order:

**Default approach (simple services):**

1. **Domain layer** — Entities, value objects, domain events, repository interfaces
2. **Application layer** — Services with business logic, DTOs
3. **Infrastructure layer** — Repository implementations, external adapters
4. **Presentation layer** — Controllers, resolvers, route definitions

**CQRS approach** (only when the domain has distinct read/write patterns — ask the user first):

1. **Domain layer** — Same as above
2. **Application layer** — Commands, queries, handlers (instead of services)
3. **Infrastructure layer** — Same as above
4. **Presentation layer** — Controllers using CommandBus/QueryBus instead of services

Load references as needed:

- `references/stack-configuration.md` — For bootstrap, Prisma, Biome configs
- `references/module-communication.md` — For event system implementation
- `references/state-isolation.md` — For entity naming and isolation checks
- `references/authentication.md` — For auth guard and session setup
- `references/testing-patterns.md` — For test structure and mocks

**Implementation rules:**

- Every module gets its own NestJS `Module` class with explicit imports/exports
- Repository interfaces live in domain layer; implementations in infrastructure
- Cross-module communication happens ONLY via events or shared contracts
- Never import a module's internal service directly from another module
- Use dependency injection for all services — no manual instantiation

### Phase 4: Validation

Verify the architecture holds before shipping.

1. **State isolation check** — Run `scripts/validate-isolation.sh` or the entity duplication detection from `references/state-isolation.md`
2. **Boundary check** — Verify no direct cross-module imports
3. **Test coverage** — Unit tests for domain, integration for boundaries
4. **Communication check** — Events flow correctly between modules
5. **Build check** — NX build graph respects module boundaries

**Exit criteria:**

- [ ] No duplicate entity names across modules
- [ ] No direct cross-module service imports
- [ ] All modules build and test independently
- [ ] Event contracts are validated
