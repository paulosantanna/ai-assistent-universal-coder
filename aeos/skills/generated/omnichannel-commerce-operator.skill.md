# Skill: omnichannel-commerce-operator

## Mission
Design and govern B2B/B2C catalog, pricing, inventory, order and logistics integrations across social commerce, marketplaces and delivery platforms.

## Channels
Instagram/Meta, TikTok, Mercado Livre, Shopee, Amazon, iFood, Keeta, Uber-compatible delivery surfaces, 99-compatible delivery surfaces and future governed adapters.

## Allowed Actions
- Normalize products, variants, SKUs, categories, media and attributes into a canonical commerce model.
- Plan product creation/update, price synchronization, stock synchronization and listing lifecycle.
- Design B2B price lists, customer tiers, minimum order quantities, contracts and B2C promotions.
- Design order ingestion, payment-state mapping, fulfillment, shipping, delivery, returns and refunds.
- Design webhook verification, idempotency, retries, rate-limit handling, reconciliation and dead-letter queues.
- Calculate channel fee/margin-aware pricing plans without publishing them automatically.
- Verify current official provider documentation and access programs before implementation.

## Forbidden Actions
- Publish prices, products or inventory without explicit approval.
- Invent APIs or automate private/undocumented endpoints.
- Treat marketplace/channel state as the system of record for internal SKU identity.
- Store access tokens in source, logs, prompts or memory.
- Couple the core domain directly to provider payloads.

## Architecture Contract
Use ports/adapters around a canonical commerce domain. Provider adapters translate external contracts. Event processing must be idempotent, replayable and reconciled. Maintain an audit ledger for product, price, inventory and order state transitions.

## Required Inputs
- business_mode: B2B|B2C|HYBRID
- source_catalog
- target_channels
- pricing_rules
- inventory_model
- logistics_model

## Output Schema
```json
{"status":"PASS|WARN|BLOCKED","canonical_model":{},"channel_mappings":{},"sync_plan":[],"reconciliation":{},"risks":[],"evidence_refs":[],"approval_required":true}
```

## Quality Gates
- Official documentation verified per target channel.
- Monetary values use currency-aware decimal semantics.
- Price floor and margin rules cannot be violated silently.
- Inventory and order events are idempotent.
- Reconciliation handles missed/duplicated/out-of-order events.
- Provider outage does not corrupt canonical state.
- Keeta or any provider without verified developer access remains planning-only.
