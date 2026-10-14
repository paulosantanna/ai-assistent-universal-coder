<!-- Package: 00_skills/(development)/wordpress-expert; relative command/resource examples resolve from that package or workspace root. -->

## First-run Beta Mapping

For each remote site, derive deterministic `site_id = sha256(canonical_base_url)`.

If `.aeos/wordpress/sites/<site-id>/beta-map.json` does not exist or fails schema validation, the **first run is mapping-only by default**:

1. establish authenticated cookie session;
2. verify target hostname and wp-admin identity without persisting user PII;
3. discover `/wp-json/`, namespaces and supported methods;
4. map WordPress version, theme mode, active theme/parent-child relation;
5. map **all** installed plugins (regular, must-use, single-file), versions and activation state — never a sampled catalog;
6. map pages, post types, navigation, templates/template parts/patterns and key settings by metadata/IDs;
7. map front-end assets, builders, custom plugin namespaces, CDN/cache/security indicators and external integrations;
8. map safe rollback/backup affordances;
9. create `beta-map.json` with no credentials, cookies, nonces, secret option values or personal user data;
10. verify map completeness and mark `mapping_state: consolidated`.

### One-shot invariant

A consolidated Beta Map is **never fully regenerated automatically**. Later runs reuse it and perform only a lightweight preflight/delta check. Full remap requires explicit `wordpress expert remap` intent or an invalid/corrupt map.
