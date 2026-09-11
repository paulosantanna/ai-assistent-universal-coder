# CodENavi Runtime Authentication Standard

Updated: 2026-09-11

## Scope

This standard applies to every AEOS skill, super-skill, MCP, playbook, adapter and Tool Router integration that authenticates to a remote/local system.

## Core rule

Credential material is usable at runtime but is never part of model context or persisted workspace state. Skills and MCPs exchange opaque `session_ref` values, not cookies/passwords/tokens.

## Universal flow

1. A governed skill selects an approved source reference.
2. `runtime-auth` opens that source into an in-memory session with TTL and optional host scope.
3. The caller receives only `session_ref` plus non-secret metadata.
4. A governed adapter such as `runtime-http` receives the session reference.
5. The Tool Router materializes the credential internally for the exact target/action.
6. Evidence records only the opaque/ref metadata and decision; raw values are never persisted.
7. Session material is destroyed on close, expiry or Tool Router shutdown.

## Approved source classes

- external cookie/cookie-jar file reference;
- environment variable reference;
- OS credential manager/keychain/secret service through an adapter;
- GitHub Actions secret reference inside CI;
- approved Vault/provider reference;
- explicit ephemeral runtime memory supplied by a trusted adapter.

A source class being approved does not imply unrestricted use: host/action/policy gates still apply.

## External cookie files

Cookie files are consumed in place. They must not be copied into the repository, `.aeos`, evidence, notebook, bundle, prompt or logs. Default policy requires an absolute path outside the tracked workspace. Supported runtime parsing includes Netscape cookie jars and common JSON browser exports; raw Cookie-header files require explicit host scope.

## Host scoping

Cookie/session material may be sent only to a target host allowed by the session. Authenticated HTTP requires HTTPS, rejects URL-embedded credentials, blocks localhost/private-network targets by default and does not automatically follow redirects.

## Model boundary

The model may see:

- provider/source type;
- opaque session reference;
- allowed host names;
- timestamps/TTL;
- non-secret success/failure state.

The model must never see:

- cookie values;
- Authorization headers;
- passwords;
- API tokens/keys;
- private key contents;
- CSRF/nonces when those values function as authentication/session material.

## MCP/skill integration

`RegistryLoader.resolveMCPs()` injects the core `runtime-auth` and `runtime-http` MCPs into every playbook's resolved MCP set. This provides universal capability without copying authentication logic into each skill.

MCP/skill code should accept `__aeosAuthSessionRef`/`session_ref` and delegate credential materialization to the Tool Router. Direct credential parameters are legacy-only and should be migrated when the adapter is touched.

## Mutation gate

Authenticated `GET`, `HEAD` and `OPTIONS` may be used for read-only mapping/preflight. `POST`, `PUT`, `PATCH` and `DELETE` through `runtime-http` require `approved=true` from the governed change path. This flag is not itself sufficient for destructive/high-risk actions; normal permission/policy/Judge/rollback gates still apply.

## Evidence and observability

Tool call audit must redact secret-like keys including cookie, authorization, nonce, password, token, private key and credential. Opaque session refs may be logged only in shortened form.

## Failure behavior

Fail closed on missing/expired session, target host mismatch, cookie file inside workspace, unsupported file format, oversized cookie file, non-HTTPS target, private-network target, redirect dependency, absent approval for mutation or any attempt to return raw secret material.
