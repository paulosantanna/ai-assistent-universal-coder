# AEOS Registries contract

Governance: CodENavi Full Workspace v2

Inherits root `AGENT.md` and `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`.

All registries, fragments, overlay indexes and manifests follow **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**.

Requirements:
- unique IDs and deterministic conflict precedence;
- every active referenced path exists;
- owner/risk/capability metadata is coherent;
- capabilities must be valid for the active capability model;
- orphaned active artifacts and dangling registry entries are defects;
- duplicate active entries require explicit audited resolution;
- overlay merge behavior must be deterministic and testable;
- no registry field may silently weaken security/governance defaults;
- changes require validation of the merged/resolved registry, not only the edited fragment.

All old registry fragments inherit this standard regardless of their creation version.
