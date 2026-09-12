# KingHost production FSM

Entry: `skills/kinghost-expert/SKILL.md`  
Updated: 2026-09-12

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
