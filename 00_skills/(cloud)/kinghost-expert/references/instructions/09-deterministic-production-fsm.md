<!-- Package: 00_skills/(cloud)/kinghost-expert; relative command/resource examples resolve from that package or workspace root. -->

## Deterministic production FSM

For code/data production publish:

`IDLE -> ENV_SELECTED -> CREDENTIALS_BOUND -> PANEL_AUTH -> INVENTORY -> SNAPSHOT -> DIFF -> DRY_RUN -> BACKUP -> APPLY -> VERIFY -> CLOSE`

`ROLLBACK` is legal after APPLY/VERIFY failure. Advance with `kinghost_control.fsm.advance`.

The existing one-command WordPress path remains:

```bash
npm run aeos:kinghost:publish -- --local-dir <wordpress-tree> --domain <existing-kinghost-domain>
```
