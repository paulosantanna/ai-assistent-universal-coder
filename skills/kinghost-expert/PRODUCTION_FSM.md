# KingHost production FSM

Entry: `skills/kinghost-expert/SKILL.md`  
Updated: 2026-09-16

`ENV_SELECTED` includes the existing KingHost domain chosen via `domain.select`. Clone happens during INVENTORY when the workspace tree is missing. APPLY uses `ftp.tree.upload` / `deploy.workspace_to_production`. The one-command operator path is playbook `kinghost-wordpress-publish` (`npm run aeos:kinghost:publish`).

States are enforced by `kinghost_control.fsm.advance` in `kinghost-control-mcp/index.mjs`.

```text
IDLE
  -> ENV_SELECTED
  -> CREDENTIALS_BOUND
  -> PANEL_AUTH
  -> INVENTORY
  -> SNAPSHOT
  -> DIFF
  -> DRY_RUN
  -> BACKUP
  -> APPLY
  -> VERIFY
  -> CLOSE
```

`ROLLBACK` is allowed after `APPLY` or `VERIFY` failure. Any other skip is `BLOCKED`.
