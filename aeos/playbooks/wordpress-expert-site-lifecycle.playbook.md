# Playbook: wordpress-expert-site-lifecycle

## Required agent

- `codenavi-agent` only.

## Required skill

- `wordpress-expert`

## Required MCPs

- `wordpress-knowledge`
- `browser`
- `filesystem-readonly`
- `git-readonly` when repository-backed deployment exists
- `test-runner-controlled` when code changes have local tests

## Flow

1. Read continuity state and resolve target URL.
2. Resolve external runtime cookie/cookie-jar reference; never load cookie contents into model context.
3. Derive site_id and check Beta Map.
4. If no valid consolidated map exists: perform one-shot read-only Beta Mapping, validate schema, persist safe map and stop or continue only under explicit same-run mutation authorization.
5. If map exists: skip full mapping and run lightweight drift/preflight.
6. Consult `wordpress-knowledge` MCP for material implementation decisions.
7. Classify requested change risk and choose supported WordPress extension point.
8. Build change/rollback plan.
9. For medium/high-risk changes, prefer staging or preview when available.
10. Apply controlled mutation through authenticated wp-admin/REST/WP-CLI/repository path available to the site.
11. Verify capability/nonce semantics for cookie-authenticated REST writes.
12. Run functional, visual/responsive, accessibility, security and cache checks appropriate to the change.
13. On failure, rollback and return `ROLLBACK_REQUIRED`/`BLOCKED` with evidence.
14. On success, update only delta metadata relevant to the existing Beta Map; do not perform full remap.

## Production PASS

PASS requires verified resulting WordPress state, front-end smoke, no leaked credential material and a valid rollback record. HTTP 200 alone is insufficient.
