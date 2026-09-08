# AEOS Scripts contract

Governance: CodENavi Full Workspace v2

Inherits root `AGENT.md` and `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`.

All scripts and guards follow **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**.

Requirements:
- deterministic/fail-closed behavior for governance checks;
- actionable errors with root cause;
- no secret echo/logging;
- no hidden mutation outside the declared scope;
- bounded filesystem/process/network behavior;
- script exit codes accurately represent success/failure;
- generated files are validated before use;
- governance guards must validate the resolved workspace state, not only happy-path samples.
