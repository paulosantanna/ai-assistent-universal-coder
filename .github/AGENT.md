# GitHub / CI contract

Governance: CodENavi Full Workspace v2

Inherits root `AGENT.md` and `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`.

All workflows, actions configuration, templates and repository automation follow **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**.

Requirements:
- governance guards execute before declaring the workspace healthy;
- build/test/eval/security failures are not suppressed or relabeled as success;
- secrets use provider secret stores/references and are never echoed;
- deployment/release jobs identify target environment and rollback/recovery strategy;
- third-party actions/dependencies are pinned/assessed according to repository policy;
- generated evidence/artifacts must not leak credentials or sensitive values;
- workflow changes are verified on the actual CI path.
