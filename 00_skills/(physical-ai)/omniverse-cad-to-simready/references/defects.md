# Defects and adaptation

## Contents

- Findings
- Evidence
- Grade

## Findings

- Original `SKILL.md` has 205 physical lines. The TLC cap is 100, so the operational body moved to `references/procedure.md`.
- Original frontmatter keys: name, description, version, license, tools, allowed-tools, permissions, compatibility, metadata.
- Original description had no `Do NOT use` boundary in the routing line.
- Scripts, STL fixtures, and the OMS signature were not copied. The workflow and reference notes were.

## Evidence

- Entrypoint pattern hits:
- L9: `allowed-tools: Read Write Bash WebFetch Env`
- Sample of relative links that do not resolve inside the upstream package (0 total):
- None in the copied markdown set.
- Scripts left upstream, not vendored:
- `shared/preflight_manifest.py`
- `shared/simready_package_check_dependencies.py`
- `shared/upstream_versions.py`
- `shared/script_utils.py`
- `shared/simready_package.py`
- `references/validate-usd-minimum/scripts/check_dependencies.py`
- `references/validate-usd-minimum/scripts/run.py`
- `references/convert-to-usd/scripts/check_dependencies.py`
- `references/convert-to-usd/scripts/run.py`
- `references/convert-to-usd/references/mujoco-usd-converter/scripts/check_dependencies.py`
- `references/convert-to-usd/references/mujoco-usd-converter/scripts/run.py`
- `references/convert-to-usd/references/urdf-usd-converter/scripts/check_dependencies.py`
- `references/convert-to-usd/references/urdf-usd-converter/scripts/run.py`
- `references/convert-to-usd/references/usd-convert-cad/scripts/check_dependencies.py`
- `references/convert-to-usd/references/usd-convert-cad/scripts/run.py`
- `references/convert-to-usd/references/usd-convert-gsplat/scripts/check_dependencies.py`
- `references/convert-to-usd/references/usd-convert-gsplat/scripts/run.py`
- `references/assemble-package-source/scripts/check_dependencies.py`
- `references/assemble-package-source/scripts/run.py`
- `references/content-agents/scripts/content_agent_client.py`
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
