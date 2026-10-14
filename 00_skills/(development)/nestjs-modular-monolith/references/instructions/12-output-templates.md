<!-- Package: 00_skills/(development)/nestjs-modular-monolith; relative command/resource examples resolve from that package or workspace root. -->

## Output Templates

When implementing a complete module, provide files in this order:

1. **Domain entities** — With module-prefixed names and business logic
2. **Repository interface** — In domain layer, defines data access contract
3. **Service** (default) or **Commands/Queries + Handlers** (if CQRS) — Implementing business rules
4. **DTOs** — Request/response with Swagger decorators and validation
5. **Repository implementation** — Prisma/TypeORM in infrastructure layer
6. **Controller** — With guards, Swagger docs, and proper HTTP codes
7. **Module definition** — NestJS module with explicit imports/exports
8. **Tests** — Unit tests for services/handlers, integration tests for boundaries
9. **Domain events** — If cross-module communication is needed

When designing architecture (not implementing), provide:

1. **Executive Summary** — Architecture overview, key decisions, rationale
2. **Bounded Contexts Map** — Responsibilities, aggregates, communication
3. **Module Interface Contracts** — Public API surface of each module
4. **Data Model** — Per-module schemas with ownership boundaries
5. **Communication Diagram** — Event flows between modules
6. **Evolution Path** — How to extract modules to microservices later
