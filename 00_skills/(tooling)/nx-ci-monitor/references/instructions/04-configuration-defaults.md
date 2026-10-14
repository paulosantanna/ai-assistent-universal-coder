<!-- Package: 00_skills/(tooling)/nx-ci-monitor; relative command/resource examples resolve from that package or workspace root. -->

## Configuration Defaults

| Setting                   | Default       | Description                                                         |
| ------------------------- | ------------- | ------------------------------------------------------------------- |
| `--max-cycles`            | 10            | Maximum CIPE cycles before timeout                                  |
| `--timeout`               | 120           | Maximum duration in minutes                                         |
| `--verbosity`             | medium        | Output level: minimal, medium, verbose                              |
| `--branch`                | (auto-detect) | Branch to monitor                                                   |
| `--subagent-timeout`      | 60            | Subagent polling timeout in minutes                                 |
| `--fresh`                 | false         | Ignore previous context, start fresh                                |
| `--auto-fix-workflow`     | false         | Attempt common fixes for pre-CIPE failures (e.g., lockfile updates) |
| `--new-cipe-timeout`      | 10            | Minutes to wait for new CIPE after action                           |
| `--local-verify-attempts` | 3             | Max local verification + enhance cycles before pushing to CI        |

Parse any overrides from `$ARGUMENTS` and merge with defaults.
