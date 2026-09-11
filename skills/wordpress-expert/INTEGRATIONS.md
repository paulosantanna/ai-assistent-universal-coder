# WordPress External Integrations

## Supported intent classes

This skill can integrate outbound destinations or documented APIs for services such as 99, Mercado Livre, Mercado Pago, Keeta, TikTok Shop/vendas, iFood, Instagram, Facebook, Threads, X/Twitter, LinkedIn, YouTube, WhatsApp and other providers.

## Icon-link mode

Use when the requirement is navigation/ordering/contact through a third-party URL rather than data/API integration.

Requirements:

- compact icon button/link instead of displaying a long URL;
- semantic `<a>` behavior, not JavaScript-only navigation;
- meaningful `aria-label` and keyboard focus;
- `target="_blank"` only when appropriate with `rel="noopener noreferrer external"`;
- prefer official brand kit/official icon;
- cache the asset locally in WordPress/theme when licensing allows;
- official favicon `.ico` is an accepted fallback, not the first choice when an official scalable asset exists;
- no random logo scraped from an unrelated site;
- preserve aspect ratio, contrast and touch target size.

## API mode

Use only when an actual provider API is required. Before implementation, retrieve current official provider documentation and establish:

- supported API/product and region;
- authentication model and OAuth scopes;
- sandbox/test environment when available;
- rate limits and idempotency;
- webhook signing/verification;
- data model and error model;
- terms/brand requirements;
- server-side secret storage;
- retry/backoff and observability;
- rollback/deactivation path.

Do not derive API endpoints from consumer URLs, Reddit comments or guesswork.

## WordPress placement

Choose the smallest durable extension point:

- navigation/social links for simple destinations;
- block pattern/custom block for reusable UI;
- child theme for theme-level presentation changes;
- custom plugin for business/integration behavior;
- server-side REST/HTTP client for secrets and provider API calls.

Never embed provider private keys, OAuth client secrets or payment credentials into frontend JavaScript, block attributes or post content.

## Commerce/payments

Payment/commerce providers are high/critical risk. Do not fabricate checkout flows. Prefer provider-supported official plugins when maintained, compatible and supply-chain reviewed; otherwise implement a custom plugin only from official API contracts with webhook verification, idempotency and secure secret handling.
