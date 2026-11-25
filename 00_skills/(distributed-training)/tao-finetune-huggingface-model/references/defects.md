# Defects and adaptation

## Contents

- Findings
- Evidence
- Grade

## Findings

- Original `SKILL.md` has 404 physical lines. The TLC cap is 100, so the operational body moved to `references/procedure.md`.
- Original frontmatter keys: name, description, license, tags, compatibility, metadata, allowed-tools.
- Original description had no `Do NOT use` boundary in the routing line.
- Platform siblings tao-setup-nvidia-gpu-host and tao-run-on-docker were not imported. Stop and name them when the host or Docker contract is missing.

## Evidence

- Entrypoint pattern hits:
- L28: `allowed-tools: Read Bash Write`
- L226: ``references/workflow-intake-preflight.md`). Optionally `rm -rf "$OUTPUT_DIR/.probe"``
- Sample of relative links that do not resolve inside the upstream package (3 total):
- `references/docker-runs.md -> ../../../platform/tao-run-on-docker/SKILL.md`
- `references/workflow-intake-preflight.md -> ../../../platform/tao-setup-nvidia-gpu-host/SKILL.md`
- `references/workflow-intake-preflight.md -> ../../../platform/tao-run-on-docker/SKILL.md`
- Scripts left upstream, not vendored:
- None.
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
| disclosure | 15 | 2 | 4 |
| verification | 10 | 2 | 3 |

Before 62.0. After 78.0. Verification stays at 3 because this workspace did not rerun GPU, cluster, or clinical jobs.
