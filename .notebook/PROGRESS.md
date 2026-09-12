# PROGRESS

Updated: 2026-09-12

## Active CI Recovery
- Objective: restore green AEOS Enterprise CI after tracking `.work/` and monitor the new `master` SHA.
- [x] RECON: run `34705050420` failed at `aeos:guard:single-agent` with `spawnSync git ENOBUFS`.
- [x] CLASSIFY: `resource_exhaustion`; not retryable; fingerprint `git ls-files -z` + default 1 MiB buffer.
- [x] PATCH: `scripts/lib/git-tracked-files.mjs`; ignore `.work/` in full-workspace + Python walk.
- [x] VERIFY: local `npm run aeos:verify` PASS (frontmatter 289, python 17, jest 48).
- [ ] AUTHORIZED_PUSH + REDISCOVER: wait for CI on the new SHA.

## Previous Mission
- Objective: align the local Rei do ABC WooCommerce account/Google-auth and cart flows with the visual reference package, while retaining native WooCommerce state and secure OAuth.
- Scope: runtime at `E:\GitHub\repos-workspace\reidoabc`; reference-only package `E:\GitHub\repos-workspace\reidoabc-wordpress` is read-only. No commit unless requested.
- Success criteria: `/my-account/` offers branded login, account creation and Google OAuth when configured; a valid cart route renders a reference-aligned native WooCommerce cart; no simulated/localStorage cart is reintroduced.

## Current Phase
- DEBRIEF

## Live Checklist
- [x] BRIEFING: target is local `http://localhost:8087`; reference package must remain unmodified.
- [x] RECON: active theme is `reidoabc-gourmet-reference`; commerce is native WooCommerce plus `reidoabc-commerce-runtime`.
- [x] RECON: `/my-account/` currently renders the default English WooCommerce login and has no registration form; `/cart/` returns 404.
- [x] PLAN: style native WooCommerce account/cart contracts with the gourmet reference, expose secure Google OAuth and repair the cart endpoint.
- [x] EXECUTE: updated the runtime theme/plugin only; the reference package was not changed.
- [x] VERIFY: PHP lint passed in the WordPress container; account/cart return HTTP 200; desktop/mobile screenshots reviewed.
- [x] DEBRIEF: continuity updated; no commit requested.

## Verification Gates
- [x] Reference package has no modifications.
- [x] `/my-account/` contains account-creation and Google-auth controls, with OAuth unavailable state handled safely.
- [x] Cart link resolves successfully and has native WooCommerce cart controls styled to the gourmet reference.
- [x] Changed PHP files pass lint; desktop/mobile visual smoke checks pass for account and desktop cart.

## Factual Log
- 2026-09-12: The active runtime routes account/cart through native WooCommerce; the inspiration package's legacy modal cart uses simulated browser storage and must not replace the real cart.
- 2026-09-12: Direct smoke: `/my-account/` is default WooCommerce English login without registration; `/cart/` is HTTP 404.
- 2026-09-12: Enabled `woocommerce_enable_myaccount_registration`; branded the native account, Google OAuth and native Cart block without reintroducing the reference's localStorage cart.
- 2026-09-12: The assigned published cart page had stale rewrite rules; `flush_rewrite_rules()` restored `/cart/`. Final endpoint smoke: account 200, cart 200. OAuth credentials are absent locally, so the Google control is safely unavailable until runtime configuration is supplied.
- 2026-09-12: Copied `nx-workspace` from `E:\GitHub\.cursor\skills\nx-workspace`. Frontmatter 278/0 invalid. Overlay load tests passed.
- 2026-09-12: Copied `subagent-creator`; remapped to lenses of `codenavi-agent`.
- 2026-09-12: Copied `tlc-plan` 0.2.0 from `E:\GitHub\.cursor\skills\tlc-plan`.
- 2026-09-12: Copied `learning-opportunities` 1.1.0 from `E:\GitHub\.cursor\skills\learning-opportunities`.
- 2026-09-12: Copied `perf-astro` from `E:\GitHub\.cursor\skills\perf-astro`.
- 2026-09-12: Copied `core-web-vitals`, `perf-lighthouse` and `perf-web-optimization`.
- 2026-09-12: Copied `security-best-practices`, `security-ownership-map` and `security-threat-model`.
- 2026-09-12: Copied `web-quality-audit` 1.0 from `E:\GitHub\.cursor\skills\web-quality-audit`.

## Active Follow-up
- Objective: make the storefront category dropdown resolve each real WooCommerce category quickly and correctly.
- [x] RECON: fixed options submitted to the home page without a category query handler.
- [x] PLAN: render current `product_cat` terms, navigate immediately to canonical archives and preserve a server-side shop fallback.
- [x] EXECUTE: runtime theme, local controls and bootstrap now use real category data and real WooCommerce products; reference remains untouched.
- [x] VERIFY: PHP/JavaScript syntax checks pass; canonical category routes return 200; fallback filtering returns only selected-category products; Store API confirms an added item and BRL totals.

## Follow-up Evidence
- 2026-09-12: Replaced the homepage's invalid static product IDs (`101`–`108`) with an idempotent local WooCommerce seed. The eight local products have valid IDs `14`–`21`, split 4/4 between `pedacos-de-tortas` and `barras-de-chocolate`.
- 2026-09-12: The header dropdown is now generated from `product_cat`; selecting a category goes immediately to its canonical archive and the submit fallback filters `/shop/` on the server.
- 2026-09-12: Cart smoke with product `14` returned Store API `items_count: 1`, item name `Pedaço de Torta Holandesa Premium`, `currency_code: BRL` and `currency_symbol: R$`.

## Active Image Integrity Follow-up
- Objective: ensure the local Rei do ABC storefront never renders a missing/broken image and serves visual assets as local SVG resources.
- [x] BRIEFING: user supplied the official Rei do ABC logo; runtime remains `E:\GitHub\repos-workspace\reidoabc`, while `reidoabc-wordpress` stays read-only.
- [x] RECON: all hero and theme icons are already local SVGs, but demo WooCommerce products lack media, the commerce-links plugin serves PNG icons, and the live logo SVG does not match the supplied official logo.
- [x] PLAN: store the provided original as a project source, replace the served logo with a responsive SVG representation, migrate plugin icons to SVG and assign valid local image attachments to all local demo products.
- [x] EXECUTE: applied asset/template/bootstrap changes only to the local runtime.
- [x] VERIFY: PHP lint passed; all 25 active SVGs parse as XML; all emitted image URLs on home/shop/cart/account and every active theme/plugin SVG return HTTP 200; every published local demo product has a valid SVG media attachment; desktop/mobile visual smoke passed.
- [x] DEBRIEF: source logo is preserved locally while the browser loads the self-contained SVG; reference package remains clean.

## Image Integrity Evidence
- 2026-09-12: The supplied original `Logo-Simples-Dourado.png` is stored in the runtime theme as the source asset. `assets/images/logo-rei-do-abc.svg` embeds it as a self-contained SVG data image, so all public logo URLs are SVG and no secondary PNG request can fail.
- 2026-09-12: Added `product-cake.svg` and `product-chocolate.svg`; bootstrap registered attachments `22` and `23` under `wp-content/uploads/reidoabc-demo/` and assigned them to products `14`–`21`. Store API product `14` returns both full and thumbnail SVG URLs.
- 2026-09-12: Migrated the six site-controls commerce icons from PNG references to local SVG files. HTTP audit returned 200 for all image URLs emitted by `/`, `/shop/`, `/cart/` and `/my-account/`, and for all 25 theme/plugin SVG assets.
- 2026-09-12: Desktop (1440px) and mobile (390px) screenshots confirm the official logo and all eight product cards render without broken-image placeholders.
