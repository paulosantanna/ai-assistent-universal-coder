# Aura Voice Tool contract

Governance: CodENavi Full Workspace v2

Inherits root `AGENT.md` and `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`.

Aura Voice operations follow **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**.

Specific rules:
- media/transcript ingestion remains bounded to authorized inputs;
- ASR/transcript output is evidence, not automatically a factual claim;
- serious/humor/mixed/ambiguous classification preserves original evidence and uncertainty;
- technical nomenclature is preserved when translation would distort meaning;
- no speaker biometric identity inference;
- corpus promotion requires authorization, provenance and validation;
- no secrets in transcript errors/evidence;
- FFmpeg/ASR execution remains argument-bounded with no arbitrary shell;
- changes require adapter tests and runtime bridge verification.
