# TLC spec versions

Updated: 2026-10-26
Entry point: `00_skills/upstream.manifest.json` entries tlc-spec-driven and tlc-spec-lean.

- Driven 4.0.0: official release `ef2672d67adebb1fc95af83e25fcba4d8cce02a7`; applies to spec-driven and tlc-spec-driven.
- Lean 2.0.0: official release `2fca1d19753fa8ec2a3449371b97e4830544461a`; applies to spec-driven-lean and tlc-spec-lean. Newer main versions are intentionally outside the request.
- 47 source resources retained with registry hashes; source snapshots immutable. Local executable helpers under scripts/ adapt Unix signals and Windows process-tree timeout cleanup.
- Native discovery, catalog, registry, policies and provenance synchronized. Existing Node invocations forward to the same Python gates.
- Local selftests: 20 killed mutants per driven package and 72 per lean package, no survivors. Structure and integrity gates pass; isolated proof success/failure/recovery and Windows timeout verified.
- Bun-specific integration unexecuted because Bun is absent; general proof execution verified separately. No independent review claimed: source verifier roles are sequential local lenses under root governance.
- Publishing request explicitly authorizes PR/merge into repository default branch master, followed by checks on the final merge SHA. No main branch exists.
- Compensation: revert the scoped PR commit through normal review; no force push or branch-protection bypass.
