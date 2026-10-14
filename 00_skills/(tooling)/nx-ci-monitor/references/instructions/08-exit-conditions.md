<!-- Package: 00_skills/(tooling)/nx-ci-monitor; relative command/resource examples resolve from that package or workspace root. -->

## Exit Conditions

Exit the monitoring loop when ANY of these conditions are met:

| Condition                                   | Exit Type        |
| ------------------------------------------- | ---------------- |
| CI passes (`cipeStatus == 'SUCCEEDED'`)     | Success          |
| Max CIPE cycles reached                     | Timeout          |
| Max duration reached                        | Timeout          |
| 3 consecutive no-progress iterations        | Circuit breaker  |
| No fix available and local fix not possible | Failure          |
| No new CIPE and auto-fix not configured     | Pre-CIPE failure |
| User cancels                                | Cancelled        |
