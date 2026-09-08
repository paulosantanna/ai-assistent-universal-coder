# AEOS Language Server / LSP contract

Governance: CodENavi Full Workspace v2

Inherits root `AGENT.md` and `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`.

All language-server/LSP capabilities follow **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**.

Requirements:
- symbol/type/reference/diagnostic claims are derived from parser/index/server evidence;
- language/version support is explicit and tested;
- no fabricated symbol resolution or API signatures;
- diagnostics distinguish syntax/type/index evidence from heuristic inference;
- project-native configuration and compiler semantics take precedence over generic assumptions;
- new language support includes fixtures/golden tests and regression evidence;
- LSP intelligence may advise changes but never substitutes for repository build/tests;
- no secret material is persisted in indexes, traces or diagnostics.
