# Defects and adaptation

## Contents

- Findings
- Evidence
- Grade

## Findings

- Original `SKILL.md` has 237 physical lines. The TLC cap is 100, so the operational body moved to `references/procedure.md`.
- Original frontmatter keys: name, description, license, metadata.
- Original description already had a negative boundary.
- Search is limited to sources already registered on a deployment the user administers. Live captioning and source deletion stay out of scope.

## Evidence

- Entrypoint pattern hits:
- No targeted anti-pattern line in the entrypoint.
- Sample of relative links that do not resolve inside the upstream package (1 total):
- `references/cli_usage.md -> ../../../../AGENTS.md`
- Scripts left upstream, not vendored:
- `scripts/select_brev_origin.sh`
- Signature files omitted: skill.oms.sig
- Eval, benchmark, and agent-identity files were not copied. They are not evidence for this workspace.

## Grade

Diagnostic rubric from `00_skills/(creation)/skill-architect/references/quality-checklist.md`. Not a measured routing accuracy.

| Dimension | Weight | Before | After |
| --- | --- | --- | --- |
| routing | 20 | 4 | 4 |
| procedure | 25 | 4 | 4 |
| examples | 15 | 2 | 4 |
| errors | 15 | 4 | 4 |
| disclosure | 15 | 2 | 4 |
| verification | 10 | 2 | 3 |

Before 64.0. After 78.0. Verification stays at 3 because this workspace did not rerun GPU, cluster, or clinical jobs.
