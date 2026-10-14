<!-- Package: 00_skills/(development)/harness-eval; relative command/resource examples resolve from that package or workspace root. -->

## Loading this skill's files

This skill is **self-contained**. Protocol, scripts, and judge prompts live under this skill directory (the folder that contains this `SKILL.md`). Resolve `SKILL_DIR` as that directory — never assume another install path.

- Read [references/PROTOCOL.md](../tlc/references/PROTOCOL.md) **completely** before the first run in a session (and again if scripts fail).
- Read [references/judge-prompts.md](../tlc/references/judge-prompts.md) when spawning Track B or Track C judges.
- Plain-language terms: [references/GLOSSARY.md](../tlc/references/GLOSSARY.md) (also embedded at the top of `04` / `07` / `10` reports).
- Claim record shape: [references/claims.schema.json](../tlc/references/claims.schema.json) (for tooling; agents do not need to load it every run).
- Run scripts as `python3 "$SKILL_DIR/scripts/<name>.py" ...`.

Run **outputs** (not protocol) go to the target repo at `.harness-eval/runs/<run-id>/`.
