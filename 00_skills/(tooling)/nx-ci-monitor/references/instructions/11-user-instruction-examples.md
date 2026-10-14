<!-- Package: 00_skills/(tooling)/nx-ci-monitor; relative command/resource examples resolve from that package or workspace root. -->

## User Instruction Examples

Users can override default behaviors:

| Instruction                                      | Effect                                        |
| ------------------------------------------------ | --------------------------------------------- |
| "never auto-apply"                               | Always prompt before applying any fix         |
| "always ask before git push"                     | Prompt before each push                       |
| "reject any fix for e2e tasks"                   | Auto-reject if `failedTaskIds` contains e2e   |
| "apply all fixes regardless of verification"     | Skip verification check, apply everything     |
| "if confidence < 70, reject"                     | Check confidence field before applying        |
| "run 'nx affected -t typecheck' before applying" | Add local verification step                   |
| "auto-fix workflow failures"                     | Attempt lockfile updates on pre-CIPE failures |
| "wait 45 min for new CIPE"                       | Override new-CIPE timeout (default: 10 min)   |
