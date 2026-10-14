# Advisory and lifecycle provider evidence

Updated: 2026-10-12
Source: IMG_2368–IMG_2377; current primary entrypoints checked during this mission.

Use the repository ecosystem and exact resolved version. Provider sources are normative for their own advisory/date claims; never substitute model memory.

- OSV: https://google.github.io/osv.dev/ — ecosystem/package/version matching and affected ranges.
- GitHub advisories: https://docs.github.com/en/code-security/security-advisories — GHSA records and package advisory context.
- NVD: https://nvd.nist.gov/developers/vulnerabilities — CVE/CPE context; confirm applicability before treating a broad match as exposure.
- endoflife.date: https://endoflife.date/docs/api/v1/ — release/product lifecycle metadata and its referenced sources.
- Official maintainer support/security pages and the target project's resolved lockfile/BOM/runtime inventory — product-specific support and installed-version evidence.

Capture provider, record ID, package/product/distribution, detected version and provenance, affected/fixed range or lifecycle date, retrieval/snapshot time and URL. Deduplicate IDs/aliases. Reconcile disagreement by source scope, distribution and freshness. Unknown coverage is an explicit result; no fabricated zero-vulnerability or support verdict.
