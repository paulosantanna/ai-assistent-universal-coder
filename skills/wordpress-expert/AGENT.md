# Local AGENT contract — wordpress-expert

This file specializes the root `AGENT.md`; it does **not** define another agent identity. All work remains owned by the canonical `codenavi-agent`.

## Mission lifecycle

Use `BRIEFING -> RECON -> PLAN -> EXECUTE -> VERIFY -> DEBRIEF`.

## First contact with a site

1. Resolve the authorized site URL and execution scope.
2. Call `wordpress.site.map_status`.
3. If no baseline exists, call `wordpress.site.map_beta` exactly once.
4. Persist only non-secret capability/architecture metadata.
5. Use that Beta map for all future missions on the same site fingerprint.

Never perform a full remap automatically after the baseline exists. Observe only the delta necessary for the current request and record it separately.

## Production mutation

Before any production write:

- load Beta baseline;
- obtain current narrow evidence for the affected resource;
- verify current official documentation for version/provider-sensitive behavior;
- produce the minimal change-set;
- define backup/rollback;
- pass Permission/Policy/Judge and required approval;
- open the runtime write gate;
- execute only the allowlisted MCP operation;
- re-read and verify remote state.

## Front-end Staff gate

For visual/frontend work, self-review the proposed change for semantic HTML, responsive layout, accessibility, cascade/design-system consistency, browser behavior, performance, cache effects, WordPress/Gutenberg conventions and rollback.

Verdicts: `APPROVED`, `NEEDS_REWORK`, `REJECTED`.

## External integrations

Distinguish an outbound icon link from a real provider API integration. A provider API requires current official provider documentation; never infer an endpoint from a consumer website or Reddit post.

## Secrets

Application Passwords, wp-admin passwords, API keys, OAuth tokens and cookies are runtime-only. Never persist them in Beta Map, knowledge cache, notebook, evidence, Git, generated code, frontend markup or tool output.

## Stop conditions

Fail closed for ambiguous target site, missing authorization, missing backup/rollback for production mutation, unsupported REST capability, stale/uncorroborated API knowledge, secret exposure, missing provider documentation or verification failure.
