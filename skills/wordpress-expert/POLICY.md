# WordPress Expert Policy

## Source authority

1. Official WordPress developer/core documentation is normative.
2. Official release/Field Guide/source reference resolves version deltas.
3. WordPress support/community documentation may supplement operational context.
4. Reddit is secondary evidence only and never defines an API contract.
5. Third-party API integrations require the current official documentation of that provider.

## Beta baseline

The Beta Map is immutable first-run knowledge for a normalized site fingerprint. Once created, automatic full remapping is denied. Later execution may collect narrow delta evidence but must not overwrite or regenerate the baseline.

## Production write levels

- `read_only`: discovery, knowledge, Beta Map read, content/settings/plugin reads.
- `medium`: draft content/media creation where rollback is trivial.
- `high`: published content, settings, plugin activation/install, navigation/template/global-style mutation.
- `critical`: production code/theme/plugin deployment, authentication changes, commerce/API integration, permanent delete.

All writes require external AEOS policy/permission decisions plus runtime gate `AEOS_WORDPRESS_MUTATION_MODE=approved-write`.

## Deletion

Default deletion is trash-first. Permanent content deletion additionally requires `AEOS_WORDPRESS_ALLOW_PERMANENT_DELETE=true` and literal confirmation `PERMANENT_DELETE`. Generic filesystem/plugin/theme/database permanent deletion is not exposed.

## wp-admin

REST Application Password credentials must never be repurposed as interactive wp-admin credentials. Interactive wp-admin requires a separate authorized browser adapter/session; cookies/passwords cannot be exported or persisted.

## Code changes

Never edit WordPress Core. Avoid production Theme/Plugin File Editor. Prefer versioned child theme, custom plugin, custom block or deployment artifact with rollback. Direct database writes are not part of this skill.

## External services

Outbound icon link and API integration are different change classes. Links may use official local-cached brand assets/favicons. API integrations require documented authentication, scopes, rate limits, webhook verification, error handling and server-side secret storage.

## Security

- SSRF guard enabled; private/local networks blocked unless explicitly enabled for an authorized environment.
- No arbitrary shell, arbitrary REST write, database write, cookie export or secret read tool.
- Download/fetch sizes and crawl pages are bounded.
- Plugin install is restricted to WordPress.org-style slug in the generic MCP operation.
- External package/plugin uploads require a separate supply-chain review.

## Verification

A successful HTTP mutation is insufficient. The skill must re-read the changed resource and, when visual behavior changes, verify frontend output/accessibility/responsive behavior using an available governed browser/testing capability.
