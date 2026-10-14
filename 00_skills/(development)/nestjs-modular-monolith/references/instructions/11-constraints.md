<!-- Package: 00_skills/(development)/nestjs-modular-monolith; relative command/resource examples resolve from that package or workspace root. -->

## Constraints

### MUST DO

- Use dependency injection for ALL services
- Validate ALL inputs via DTOs with `class-validator`
- Define repository interfaces in domain layer, implement in infrastructure
- Prefix entities with module name (e.g., `BillingPlan`, not `Plan`)
- Use events for cross-module communication
- Document module public API via exports in NestJS module
- Write unit tests for services or command/query handlers
- Use environment variables for ALL configuration
- Document APIs with Swagger decorators (REST) or tRPC router types

### MUST NOT DO

- ❌ Share database tables across modules
- ❌ Import internal services from another module directly
- ❌ Use `any` type — leverage TypeScript strict mode
- ❌ Create circular dependencies between modules
- ❌ Use Node.js EventEmitter for production inter-module communication
- ❌ Use generic entity names (`User`, `Plan`, `Item`) without module prefix
- ❌ Hardcode configuration values
- ❌ Skip error handling — use domain-specific exceptions
- ❌ Export internal services that should stay private to a module
- ❌ Access shared mutable state across modules
- ❌ Force CQRS on modules that don't need it — start simple
