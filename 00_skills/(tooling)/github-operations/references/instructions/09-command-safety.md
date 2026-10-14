<!-- Package: 00_skills/(tooling)/github-operations; relative command/resource examples resolve from that package or workspace root. -->

## Command safety

Use structured argument arrays and repository-root validation. Do not construct shell command strings from untrusted input, do not use `shell=true`, and reject control operators/path traversal/protocol handlers outside policy.
