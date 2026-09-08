# .agents compatibility contract

Governance: CodENavi Full Workspace v2

This subtree inherits root `AGENT.md` and `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`.

`.agents/skills` is a compatibility/mirror surface. It may expose skill contracts to external agent runtimes but must not become an independent source of truth that diverges from canonical AEOS governance.

All mirrored skills follow **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**, preserve bounded capabilities, evidence, secret handling, freshness and verification requirements, and must never weaken the canonical skill contract.

When a mirror conflicts with a canonical contract, the canonical stricter contract wins and the mirror must be reconciled.
