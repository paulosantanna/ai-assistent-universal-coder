<!-- Package: 00_skills/(development)/python-bug-solver-skill; relative command/resource examples resolve from that package or workspace root. -->

## Documentation Intelligence

Before proposing a Python fix, detect the project Python version from runtime files, tool config, lockfiles, CI or source evidence. Query `docs-python-current` for language, stdlib, typing, packaging and version behavior claims.

Use documentation evidence together with traceback and repository evidence. If the Python version cannot be detected or docs evidence is unavailable, return `BLOCKED` or `REVIEW` instead of guessing.
