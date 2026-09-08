# AEOS Runtime contract

Governance: CodENavi Full Workspace v2

Inherits root `AGENT.md` and `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`.

Runtime routers, loaders, engines and executors must enforce the lifecycle and governance rather than merely document it.

Requirements:
- fail closed on unknown skill/tool/capability/action;
- enforce active skill/playbook context and registered capabilities;
- preserve Judge/approval/rollback gates;
- bound time, output and resource use;
- redact secrets/errors before evidence/logging;
- separate declarative contracts from executable implementations;
- validate merged registry/config state;
- surface root cause rather than swallowing failures;
- produce deterministic evidence for verification when possible;
- shutdown/cleanup adapters and ephemeral sessions safely.

Runtime changes follow **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF** and must run the repository-native build/tests before completion.
