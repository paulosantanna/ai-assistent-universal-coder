# HANDOFF

Updated: 2026-09-11

## Objective
- Maintain AEOS with workspace-wide runtime authentication, governed GitHub/DevOps operations, and the new WordPress Knowledge/Expert capability under the single `codenavi-agent` architecture.

## Last verified functional state
- Branch: `master`.
- Functional merge commit: `096c9edc5c6a61dcff81a21bfd83a7a0bab00187`.
- PR #28 was merged after final head `321a6ff4e3967361b3eee56a9899877923a4a580` passed AEOS Enterprise CI run #154.
- Push validation on merged `master`: AEOS Enterprise CI run #155, `completed/success`.
- Check runs on merge SHA: exactly one visible required execution, `aeos-quality-gates`, `completed/success`.
- Run #155 generated both AEOS evidence and a verified Work Bundle artifact.
- Superseded parallel WordPress PR #27 was closed without merge.

## What is now canonical
- `runtime-auth`: universal in-process credential-session broker available to resolved playbooks.
- `runtime-http`: authenticated HTTPS bridge using opaque session refs; raw Cookie material stays inside Tool Router/runtime.
- External cookie/cookie-jar files may be consumed in place at runtime but cannot be copied into tracked/persisted workspace artifacts.
- Active overlay fragments for skills/playbooks/MCPs/LCPs are loaded by runtime.
- `wordpress-knowledge`: evidence-first WordPress knowledge MCP; official WordPress sources are normative, Reddit is community evidence.
- `wordpress-expert`: Staff-level super-skill for mapping and governed WordPress creation/change/production work.
- WordPress Beta Mapping is full/read-only only on the first valid run per site; later operations reuse the consolidated map and perform lightweight drift/preflight.

## Security invariants
- Raw credentials are never model context, evidence, notebook, memory, Git history or Work Bundle content.
- Session refs are opaque and short-lived; session material is destroyed on close/expiry/router shutdown.
- Authenticated HTTP requires HTTPS, target host scope and bounded output; remote mutation still goes through normal AEOS approval/policy/Judge/rollback gates.
- Repository deletion remains permanently denied/manual-only.

## Known follow-up
- Existing specialized adapters may still use older direct credential plumbing. Do not mass-rewrite them solely for consistency; when an adapter is materially changed, migrate it to Runtime Auth session refs and preserve backward compatibility only where required.

## Evidence pointers
- `references/CODENAVI_RUNTIME_AUTH_STANDARD.md`
- `runtime/src/kernel/runtime-auth-broker.ts`
- `runtime/src/kernel/tool-router.ts`
- `runtime/src/kernel/registry-loader.ts`
- `aeos/mcps/runtime-auth.mcp.yaml`
- `aeos/mcps/runtime-http.mcp.yaml`
- `skills/wordpress-expert/`
- `aeos/mcp-servers/wordpress-knowledge-mcp.mjs`
- `aeos/playbooks/wordpress-expert-site-lifecycle.playbook.md`
- `tests/node/runtime-auth-broker.test.cjs`
- GitHub PR #28 / Actions runs #154 and #155
