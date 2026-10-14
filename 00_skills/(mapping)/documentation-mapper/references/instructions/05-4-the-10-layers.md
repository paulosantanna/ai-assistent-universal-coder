<!-- Package: 00_skills/(mapping)/documentation-mapper; relative command/resource examples resolve from that package or workspace root. -->

## 4. The 10 Layers

Analyze EVERY layer. No layer may be skipped. If a layer has no content, document it as "NOT FOUND" with evidence.

### Layer 1 — Infrastructure

Map: servers, networks, cloud providers, containers, orchestration, load balancers, DNS, storage, certificates, regions.

Evidence: Dockerfiles, docker-compose.yml, Kubernetes manifests, Terraform files, cloud configs, nginx.conf, .env samples, package.json engines.

### Layer 2 — Data & Persistence

Map: databases (MongoDB, ChromaDB, PostgreSQL, Redis, etc.), collections, tables, schemas, indexes, relationships, data flow, ETL pipelines, migrations, seeds, backups.

Evidence: schema files, migration files, Prisma/SQLAlchemy/TypeORM models, seed scripts, connection configs, mongo CLI output, collection names.

### Layer 3 — Backend & API

Map: services, controllers, routes, endpoints (method + path + params + response), middleware, error handling, authentication, authorization, rate limiting, webhooks.

Evidence: route files, controller files, OpenAPI/Swagger specs, Postman collections, middleware registrations.

### Layer 4 — Frontend & Presentation

Map: pages, components, routing, state management, API consumption, UI framework, theming, i18n, forms, validation.

Evidence: component files, router config, store files, hook files, page files, layout files.

### Layer 5 — Business Logic & Domain

Map: domain models, services, use cases, business rules, workflows, state machines, validation rules, calculations, policies.

Evidence: service files, domain files, business rule files, workflow files, test cases.

### Layer 6 — Integrations & External Systems

Map: third-party APIs, MCP connections, webhooks, message queues, event buses, external services, payment gateways, email, SMS, file storage.

Evidence: integration files, webhook handlers, queue consumers, MCP configs, external API clients.

### Layer 7 — Security & Compliance

Map: authentication (JWT, OAuth, SAML), authorization (RBAC, ABAC), encryption, secrets management, CSP, CORS, input validation, audit logs, rate limiting, HIPAA/GDPR/LGPD.

Evidence: auth middleware, guard files, permission files, encryption utilities, secret configs, security headers.

### Layer 8 — DevOps & CI/CD

Map: pipelines, build scripts, deployment scripts, environments (dev/staging/prod), containers, versioning, artifacts, changelog, release process.

Evidence: CI/CD YAML files, GitHub Actions, Dockerfiles, Makefiles, deploy scripts, .gitignore, .dockerignore.

### Layer 9 — Observability & Monitoring

Map: logging, metrics, tracing, alerting, dashboards, health checks, error tracking, APM, SLIs, SLOs.

Evidence: logger config, monitoring config, health endpoints, alert rules, dashboard JSONs.

### Layer 10 — Governance & Documentation

Map: project docs, ADRs, coding standards, contribution guides, license, code of conduct, API docs, architecture docs, runbooks, onboarding docs.

Evidence: README, CONTRIBUTING, LICENSE, ADR files, docs/ directory, wiki pages.

---
