# Defects and adaptation

## Contents

- Findings
- Evidence
- Grade

## Findings

- Original `SKILL.md` has 212 physical lines. The TLC cap is 100, so the operational body moved to `references/procedure.md`.
- Original frontmatter keys: name, description, version, license, tools, metadata.
- Original description had no `Do NOT use` boundary in the routing line.
- Credential and pod scripts were not copied. Structural-defect flow has no crop_max_emit knob; do not invent one.

## Evidence

- Entrypoint pattern hits:
- No targeted anti-pattern line in the entrypoint.
- Sample of relative links that do not resolve inside the upstream package (0 total):
- None in the copied markdown set.
- Scripts left upstream, not vendored:
- `scripts/preflight_pod_template.sh`
- `scripts/preflight_urls.sh`
- `scripts/preflight_credentials.sh`
- `scripts/render_defect_spec.py`
- `scripts/pick_best_step.sh`
- Signature files omitted: skill.oms.sig
- Eval, benchmark, and agent-identity files were not copied. They are not evidence for this workspace.

## Grade

Diagnostic rubric from `00_skills/(creation)/skill-architect/references/quality-checklist.md`. Not a measured routing accuracy.

| Dimension | Weight | Before | After |
| --- | --- | --- | --- |
| routing | 20 | 2 | 4 |
| procedure | 25 | 4 | 4 |
| examples | 15 | 2 | 4 |
| errors | 15 | 4 | 4 |
| disclosure | 15 | 2 | 4 |
| verification | 10 | 2 | 3 |

Before 56.0. After 78.0. Verification stays at 3 because this workspace did not rerun GPU, cluster, or clinical jobs.
