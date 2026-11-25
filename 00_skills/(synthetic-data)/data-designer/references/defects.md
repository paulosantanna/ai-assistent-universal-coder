# Defects and adaptation

## Contents

- Findings
- Evidence
- Grade

## Findings

- Original `SKILL.md` has 93 physical lines. The TLC cap is 100, so the operational body moved to `references/procedure.md`.
- Original frontmatter keys: name, description, license, metadata.
- Original description had no `Do NOT use` boundary in the routing line.
- Removed the instruction to skip workspace reconnaissance and the `$ARGUMENTS` slash-command slot. The dataset description is the user's request.
- Interactive and autopilot workflows stay in references. Package installation still requires permission.

## Evidence

- Entrypoint pattern hits:
- L11: `Do not explore the workspace first. The workflow's Learn step gives you everything you need.`
- L17: `$ARGUMENTS`
- Sample of relative links that do not resolve inside the upstream package (0 total):
- None in the copied markdown set.
- Scripts left upstream, not vendored:
- `scripts/get_person_object_schema.py`
- Signature files omitted: skill.oms.sig
- Eval, benchmark, and agent-identity files were not copied. They are not evidence for this workspace.

## Grade

Diagnostic rubric from `00_skills/(creation)/skill-architect/references/quality-checklist.md`. Not a measured routing accuracy.

| Dimension | Weight | Before | After |
| --- | --- | --- | --- |
| routing | 20 | 2 | 4 |
| procedure | 25 | 4 | 4 |
| examples | 15 | 4 | 4 |
| errors | 15 | 4 | 4 |
| disclosure | 15 | 3 | 4 |
| verification | 10 | 2 | 3 |

Before 65.0. After 78.0. Verification stays at 3 because this workspace did not rerun GPU, cluster, or clinical jobs.
