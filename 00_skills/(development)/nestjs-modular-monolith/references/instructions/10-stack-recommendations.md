<!-- Package: 00_skills/(development)/nestjs-modular-monolith; relative command/resource examples resolve from that package or workspace root. -->

## Stack Recommendations

When the user hasn't specified preferences, recommend this stack with rationale:

| Component    | Recommendation                        | Why                                                                    |
| ------------ | ------------------------------------- | ---------------------------------------------------------------------- |
| HTTP Adapter | **Fastify**                           | 2-3x faster than Express, better TS support, plugin architecture       |
| ORM          | **Prisma**                            | Type-safe queries, declarative schema, excellent migrations            |
| API Layer    | **tRPC** or **REST+Swagger**          | tRPC for full-stack TS; REST+Swagger for public APIs                   |
| Monorepo     | **NX**                                | Task orchestration, affected commands, module boundaries               |
| Linting      | **Biome**                             | 35x faster than Prettier, single tool for format+lint                  |
| Testing      | **Jest** (unit) + **Supertest** (E2E) | NestJS native support, well-documented                                 |
| Auth         | **Passport/JWT** or **Better Auth**   | Passport for standard flows; Better Auth for modern, plugin-based auth |
| Complexity   | **Simple services** (default)         | CQRS only when domain has distinct read/write patterns                 |

Always ask the user before assuming. Present alternatives with tradeoffs.
