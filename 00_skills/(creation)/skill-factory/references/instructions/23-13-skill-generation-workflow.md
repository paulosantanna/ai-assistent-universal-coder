<!-- Package: 00_skills/(creation)/skill-factory; relative command/resource examples resolve from that package or workspace root. -->

## 13. Skill generation workflow

When invoked:

1. Parse the user request.
2. Normalize the desired name.
3. Extract purpose, inputs, outputs and constraints.
4. Determine risk.
5. Select architecture level.
6. Generate `SKILL.md`.
7. Generate `references/package-notes.md`.
8. Generate optional scripts, schemas, templates and tests.
9. Generate learning modules only when justified.
10. Run `scripts/skill_factory.py validate`.
11. Run generated tests when possible.
12. Generate `MANIFEST.json`.
13. Return package location and validation evidence.

---
