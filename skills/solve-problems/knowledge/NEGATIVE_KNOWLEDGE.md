# NEGATIVE_KNOWLEDGE.md

Do not repeat these repair failures:

- Adding comments to source code while fixing an error.
- Leaving unused imports, orphan variables, dead assignments or unused files after a fix.
- Solving a local symptom by changing architecture, package layout or framework boundaries.
- Weakening tests, deleting assertions or skipping failures to obtain a pass.
- Applying a fix before reading project memory and affected code.
- Treating pod phase, a single log line or a single dashboard as complete root cause evidence.
- Adding dependencies when the existing language runtime or project utilities can solve the defect.
