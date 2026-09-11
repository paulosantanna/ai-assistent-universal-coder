# WordPress Expert Policy

## Risk classes

- read_only: knowledge lookup, Beta Mapping, inventory, page/source inspection.
- low: local code generation, documentation, preview-only layout proposal.
- medium: content/layout/plugin/theme configuration mutation with deterministic rollback.
- high: production plugin/theme install/update, code deployment, settings/security/cache changes, payment/order integration.
- destructive: content/plugin/theme deletion or database mutation; explicit approval + backup required.

## First-run policy

`beta-map.json` absent/invalid -> full read-only Beta Mapping required.

`beta-map.json` consolidated -> full mapping forbidden by default; only lightweight delta/preflight. `force_remap` requires explicit user intent.

## Production policy

Production mutation requires target verification, authenticated cookie session, capability check, rollback, scoped plan and post-change smoke. When a staging path exists and risk is medium/high, staging-first is preferred unless the user explicitly accepts live-only risk.

## WordPress extension policy

Do not edit WordPress core for feature work. Prefer supported settings, blocks/site editor, child theme/site-specific plugin, then custom plugin/block. Direct DB/file edits are last resort.

## Security policy

Cookie jar is an approved runtime secret source. Raw cookie/nonces/passwords/tokens never persist. For cookie-authenticated REST writes, obtain/use a valid WordPress REST nonce through the authenticated session and verify capabilities.

## Third-party integration policy

Provider links/APIs for 99, Mercado Livre, Mercado Pago, Keeta, TikTok, iFood and social networks must use current provider documentation. Prefer compact branded icon/favico UI with accessible labels and safe external-link attributes. Secrets belong in runtime/server-side configuration, never front-end markup.
