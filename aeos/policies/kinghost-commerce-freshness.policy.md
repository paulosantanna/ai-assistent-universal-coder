# KingHost Commerce Knowledge Freshness Policy

## Purpose
Prevent AEOS from treating hosting, framework or commerce-channel knowledge as timeless facts.

## Rules
1. Official documentation is the default authority for vendor capabilities and APIs.
2. Every material recommendation must retain source URL, retrieval timestamp and provider/version context when available.
3. Knowledge older than 30 days is stale for planning and must be refreshed when the topic is likely to change.
4. Before any production, DNS, catalog, price, inventory, order or deployment mutation, refresh the relevant first-party documentation regardless of cache age.
5. Undocumented endpoints, reverse-engineered private APIs, scraped credentials and browser-session impersonation are forbidden.
6. If a provider has no verified public developer surface, AEOS may design an adapter boundary but must mark execution BLOCKED until official access is verified.
7. Conflicting sources are resolved in this order: current official API docs, current official help/docs, standards/specifications, first-party engineering material, trusted secondary material.
8. Marketplace and delivery integrations must account for authentication scopes, rate limits, pagination, retries, idempotency, webhook verification, reconciliation and deprecation notices.
9. KingHost recommendations must be constrained by the customer's actual hosting plan and enabled services; never assume SSH, Node.js, a database engine, runtime version or resource limit.

## High-risk stop conditions
- stale or missing official documentation;
- unknown hosting plan constraints;
- missing backup/rollback path;
- destructive query without explicit approval;
- price or inventory publication without validation;
- credential material present in logs or prompts;
- integration depends on an undocumented/private endpoint.
