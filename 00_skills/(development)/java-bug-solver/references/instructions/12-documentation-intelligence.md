<!-- Package: 00_skills/(development)/java-bug-solver; relative command/resource examples resolve from that package or workspace root. -->

## Documentation Intelligence

Before proposing a Java fix, detect the project Java version from build files, toolchains, runtime config or source evidence. Query the matching documentation MCP before making API, deprecation, removal or migration claims:

- `docs-java-11`
- `docs-java-17`
- `docs-java-21`
- `docs-java-25`
- `docs-java-26`

Use documentation evidence together with stack trace and repository evidence. If the Java version cannot be detected or the required docs MCP is unavailable, return `BLOCKED` or `REVIEW` instead of guessing.
