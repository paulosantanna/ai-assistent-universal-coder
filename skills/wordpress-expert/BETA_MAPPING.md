# WordPress Beta Mapping

## Purpose

Create a durable first-contact baseline for each authorized WordPress site so later work does not repeatedly rediscover the entire installation.

## Identity

The site identity is `sha256(normalized_site_url)[0:20]`. The baseline lives at:

`.aeos/wordpress/sites/<site_fingerprint>/beta-map.json`

The file contains no credentials or cookies.

## First run

`map_status -> map_beta -> consolidate -> reuse`

`wordpress.site.map_beta` first checks the baseline path. If it exists, the call returns `REUSED` and performs no full network remap. If it does not exist, it discovers the WordPress capability surface and writes the baseline atomically.

## Baseline scope

Capture only architecture/capability metadata needed for safe future operations:

- normalized URL and fingerprint;
- REST availability, namespaces and route prefixes;
- WordPress version hint when publicly exposed;
- post/content type metadata;
- active theme metadata when permitted;
- plugin metadata when permitted;
- allowlisted settings metadata when permitted;
- templates/template parts/navigation metadata when supported;
- advertised Abilities API surface when present;
- authentication mode/capability status without credential values.

Do not persist post bodies, customer/order data, user lists, passwords, Application Passwords, API keys, cookies or authorization headers.

## Later runs

Use `wordpress.site.map_get` first. Inspect only the narrow current delta required for the requested change. Store delta evidence in execution evidence/reporting, not by rewriting the Beta baseline.

## Structural drift

A large upgrade, theme replacement or platform migration can make the Beta baseline historically stale. Preserve it as the original first-contact map. Create an explicit migration/delta report rather than silently overwriting it.

## Failure behavior

If the site cannot be reached or required permissions are absent on the first run, the map may record unavailable capability probes, but must not claim those capabilities are absent from WordPress. Retry missing individual evidence later as a delta; do not erase the original mapping event.
