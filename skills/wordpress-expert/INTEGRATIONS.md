# External Integrations

## Supported families

- delivery/order: 99, Keeta, iFood;
- marketplace: Mercado Livre, TikTok commerce/sales;
- payments: Mercado Pago;
- social: Instagram, Facebook, TikTok, Threads, X/Twitter, YouTube, WhatsApp and provider-specific additions.

## Integration modes

1. external deep link/button;
2. provider API from server-side plugin code;
3. webhook endpoint;
4. checkout/payment handoff;
5. embedded provider widget only when security/privacy/terms permit;
6. catalog/order synchronization when a supported API exists.

## Front-end representation

Prefer compact branded icon/favicon UI instead of exposing long raw URLs. For every icon-only item:

- accessible `aria-label` or visible tooltip;
- keyboard focus state;
- adequate target size and contrast;
- text fallback for missing asset;
- `rel="noopener noreferrer"` on new external tabs where applicable;
- sanitized/validated URL;
- provider-approved or locally stored brand asset where licensing permits;
- avoid unstable third-party hotlinking when a controlled asset is available.

## Security

Provider API keys/tokens never enter HTML/JS/theme source. Keep sensitive integration logic server-side in a plugin or approved secret-backed adapter. Verify signatures for webhooks where provider supports them.
