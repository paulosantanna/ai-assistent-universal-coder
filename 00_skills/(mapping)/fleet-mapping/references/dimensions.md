# Ten evidence dimensions

Updated: 2026-10-12
Source: IMG_2385–IMG_2436. Read for each repository map.

| Dimension | Capture and verify |
| --- | --- |
| 1. technologies and versions | language/framework/library/runtime/build; exact version; source manifest/lockfile/BOM or runtime provenance |
| 2. architecture | observed layers, execution/deployment shape, sync/async integration style; distinguish intended from observed |
| 3. business purpose | users, responsibilities, journeys and outcomes backed by source/domain evidence |
| 4. application flow | entrypoint through code, external call, data and result/error; include branch/failure paths |
| 5. data model | entities/tables/schema, owners, keys, constraints, persistence and sensitive-data boundaries |
| 6. configuration/deployment | actual environments, configuration keys, jobs, containers/resources and secret references only |
| 7. observability/operation | logs, metrics, traces, probes, alerts, runbooks, failure propagation and accountable owner |
| 8. interfaces/dependencies | concrete caller/callee, protocol/route/topic, contract, sync/async semantics and cross-repository evidence |
| 9. vulnerabilities | exact package/version/source, advisory affected range, severity, fixed version and scanner/provider freshness |
| 10. obsolescence | product/distribution/release, official support/EOL date, source/freshness and unknown records |

Use full repository-relative path plus line location for factual claims. The claimed value must occur at that pointer. Mark each dimension investigated, unknown, not applicable with reason, or pending. Never replace an investigated value with null because the current stage did not look. Summarize coverage against the complete intake list; an incomplete fleet is not a complete map.
