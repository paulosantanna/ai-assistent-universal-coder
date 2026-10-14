<!-- Package: 00_skills/(tooling)/nx-ci-monitor; relative command/resource examples resolve from that package or workspace root. -->

## Error Handling

| Error                    | Action                                                                                |
| ------------------------ | ------------------------------------------------------------------------------------- |
| Git rebase conflict      | Report to user, exit                                                                  |
| `nx apply-locally` fails | Report to user, attempt manual patch or exit                                          |
| MCP tool error           | Retry once, if fails report to user                                                   |
| Subagent spawn failure   | Retry once, if fails exit with error                                                  |
| No new CIPE detected     | If `--auto-fix-workflow`, try lockfile update; otherwise report to user with guidance |
| Lockfile auto-fix fails  | Report to user, exit with guidance to check CI logs                                   |
