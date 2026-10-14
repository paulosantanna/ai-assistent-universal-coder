# Repository Mapping with AEOS

## Objective

Repository mapping creates an evidence-backed model of a codebase before AEOS changes it. The result must be useful to both humans and agents and must distinguish **observed**, **inferred** and **unknown** facts.

## Mapping contract

Never map a repository by reading only its README. The README is one source, not ground truth.

Use code, manifests, tests, configuration, CI/CD, infrastructure, schemas and runtime evidence where available.

## Phase 1 — Identity and boundary

Capture:

- repository name and purpose;
- business capability/domain;
- owners/consumers when observable;
- monorepo vs single service/library/application;
- supported environments;
- release/deployment unit;
- explicit non-responsibilities.

Output: a concise repository context statement.

## Phase 2 — Technology fingerprint

Detect rather than assume:

- languages and versions;
- frameworks;
- package/build systems;
- runtime/JDK/Node versions;
- dependency manifests/lockfiles;
- containers;
- IaC;
- databases/storage;
- messaging/event technology;
- API protocols;
- frontend stack;
- test frameworks;
- observability stack.

Record the evidence path for important claims.

## Phase 3 — Structural map

Identify:

- executable entry points;
- modules/packages;
- public interfaces;
- dependency direction;
- shared libraries;
- generated/vendor code boundaries;
- configuration roots;
- migrations/schemas;
- test organization.

Do not equate folder structure with architecture without verifying call/dependency relationships.

## Phase 4 — Runtime and integration map

Map:

- inbound HTTP/GraphQL/gRPC/events/jobs/files;
- outbound APIs/events/queues/files;
- database/storage access;
- scheduled jobs;
- caches;
- identity/auth providers;
- third-party/provider dependencies;
- retries/timeouts/circuit breakers where observable;
- webhook/event flows.

For each integration, capture protocol, direction, purpose, authentication mode if safely observable and failure implications. Never record secret values.

## Phase 5 — Data map

Identify:

- major entities;
- source of truth;
- read/write ownership;
- persistence boundaries;
- migrations;
- consistency model;
- sensitive/regulated data categories when inferable from schema/domain;
- reconciliation/idempotency mechanisms.

Avoid copying real PII into documentation or notebook artifacts.

## Phase 6 — Security map

Map:

- trust boundaries;
- authentication;
- authorization;
- privileged operations;
- secret references;
- input validation boundaries;
- network exposure;
- dependency risk;
- data-at-rest/in-transit controls where observable;
- audit/evidence mechanisms.

Unknown controls must be marked unknown, not assumed secure.

## Phase 7 — Delivery and operations

Map:

- local build/run process;
- CI workflows;
- branch/release strategy if observable;
- artifact generation;
- deployment target;
- environment configuration;
- health checks;
- logging/metrics/tracing;
- alerting references;
- backup/recovery/rollback;
- operational runbooks.

## Phase 8 — Verification baseline

Determine what currently proves repository health:

- build;
- lint/static/type checks;
- unit tests;
- integration tests;
- contract tests;
- end-to-end tests;
- security scans;
- performance tests;
- architecture tests;
- smoke tests.

Run safe baseline checks when the mission permits. Record existing failures separately from failures introduced by later work.

## Phase 9 — Architecture assessment

Create an evidence-backed view of:

- system context;
- containers/services;
- important components;
- dependency graph;
- data flow;
- trust boundaries;
- single points of failure;
- high-coupling/high-change areas;
- scaling constraints;
- operational failure propagation.

Every architectural component or relationship should be classified as:

`observed | inferred | unknown`

## Phase 10 — Notebook seeding

Update `.notebook/INDEX.md` and add only durable high-value notes.

Good notebook topics:

- non-obvious architectural pattern;
- important flow entry point;
- recurring gotcha;
- domain invariant;
- critical dependency relationship;
- verified operational constraint.

Bad notebook content:

- copied source code;
- giant file inventories;
- transient command output;
- secrets;
- speculation presented as fact;
- duplicated README text.

## Phase 11 — Documentation generation

Use the evidence gathered above to generate only useful documents. A typical output can include:

- repository overview;
- architecture/context/component views;
- integration catalog;
- data-flow documentation;
- local development/build/test guide;
- deployment/operations guide;
- security/trust-boundary overview;
- ADRs for important decisions;
- modernization/risk backlog.

Use `docs-writer` after reconnaissance/analysis, not as a substitute for them.

## Mapping completeness score

A repository is sufficiently mapped for ordinary engineering work when the following are evidence-backed or explicitly marked unknown:

| Area | Required |
|---|---|
| Purpose/boundary | Yes |
| Build/runtime | Yes |
| Entry points/modules | Yes |
| Dependencies | Yes |
| External integrations | Yes |
| Data/persistence | Yes |
| Security/trust boundaries | Yes |
| CI/CD/deployment | Yes |
| Tests/verification | Yes |
| Observability/operations | Yes |
| Architecture risks | Yes |
| Notebook pointers | Yes |

Mapping is not complete merely because every row has text. Claims must be traceable to evidence.

## Suggested output

```text
Repository Map
├── Context
├── Technology fingerprint
├── Entry points
├── Modules/dependency direction
├── Runtime integrations
├── Data ownership/flows
├── Security/trust boundaries
├── Build/CI/CD/deployment
├── Verification baseline
├── Observability/operations
├── Architecture risks
├── Unknowns
└── Evidence pointers
```

## Remapping

Do not fully remap on every mission. Use incremental reconnaissance. Remap the affected dimensions when:

- major framework/runtime changes;
- module/service boundaries change;
- new persistence/integration is added;
- authentication/authorization changes;
- deployment topology changes;
- notebook/documentation evidence becomes stale.
