# Playbook: wordpress-expert-site-lifecycle

## Required agent

- `codenavi-agent` only.

## Required skill

- `wordpress-expert`

## Required MCPs

- `runtime-auth` (core-injected for every playbook)
- `runtime-http` (core-injected for every playbook)
- `wordpress-knowledge`
- `browser`
- `filesystem-readonly`
- `git-readonly` when repository-backed deployment exists
- `test-runner-controlled` when code changes have local tests

## Flow

1. Read continuity state and resolve target URL.
2. Open the external runtime cookie/cookie-jar through `runtime-auth`; retain only the opaque `session_ref` in skill context.
3. Use `runtime-http` with that session for authenticated HTTPS preflight (`/wp-admin/`, `/wp-json/`, REST `OPTIONS`) without exposing the Cookie header.
4. Derive site_id and check Beta Map.
5. If no valid consolidated map exists: perform one-shot read-only Beta Mapping, validate schema, persist safe map and stop or continue only under explicit same-run mutation authorization.
6. If map exists: skip full mapping and run lightweight drift/preflight.
7. Consult `wordpress-knowledge` MCP for material implementation decisions.
8. Classify requested change risk and choose supported WordPress extension point.
9. Build change/rollback plan.
10. For medium/high-risk changes, prefer staging or preview when available.
11. Apply controlled mutation through `runtime-http`, authenticated browser/wp-admin, REST/WP-CLI/repository path available to the site. Runtime HTTP POST/PUT/PATCH/DELETE requires `approved=true` plus normal AEOS gates.
12. Verify capability/nonce semantics for cookie-authenticated REST writes; a nonce may be consumed in runtime but must not be persisted as durable evidence.
13. Run functional, visual/responsive, accessibility, security and cache checks appropriate to the change.
14. On failure, rollback and return `ROLLBACK_REQUIRED`/`BLOCKED` with evidence.
15. On success, update only delta metadata relevant to the existing Beta Map; do not perform full remap.
16. Close the runtime auth session when the operation finishes.

## Production PASS

PASS requires verified resulting WordPress state, front-end smoke, no leaked credential material and a valid rollback record. HTTP 200 alone is insufficient.
