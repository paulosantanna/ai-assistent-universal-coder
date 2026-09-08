# AEOS Config / Policy contract

Governance: CodENavi Full Workspace v2

Inherits root `AGENT.md` and `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`.

Configuration, policies, permissions, allowlists and denylists follow **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**.

Rules:
- deny-by-default for privileged/destructive/network/secret operations;
- precedence and environment-specific overrides must be explicit;
- no hidden override may weaken root governance;
- capabilities used by agents/skills/playbooks must exist in the active capability model;
- production write paths require explicit approval/Judge/rollback where configured;
- configuration changes must be validated against merged runtime behavior, not just YAML syntax;
- secret values never belong in committed configuration; only references/identifiers may be durable.

Legacy configuration inherits this contract automatically.
