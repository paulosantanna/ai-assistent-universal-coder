# Defects and adaptation

## Contents

- Findings
- Evidence
- Grade

## Findings

- Original `SKILL.md` has 451 physical lines. The TLC cap is 100, so the operational body moved to `references/procedure.md`.
- Original frontmatter keys: name, description, license, metadata.
- Original description had no `Do NOT use` boundary in the routing line.
- Credential preflight scripts were not copied. Do not echo keys. OSMO submission waits for confirmation.

## Evidence

- Entrypoint pattern hits:
- No targeted anti-pattern line in the entrypoint.
- Sample of relative links that do not resolve inside the upstream package (0 total):
- None in the copied markdown set.
- Scripts left upstream, not vendored:
- `scripts/prepare_demo_assets.sh`
- `scripts/pl_original_worker.sh`
- `scripts/llm_server.sh`
- `scripts/generate_configs.py`
- `scripts/pre_submit_guard.py`
- `scripts/endpoint_common.sh`
- `scripts/vlm_server.sh`
- `scripts/osmo_barrier.py`
- `scripts/render_side_by_side.sh`
- `scripts/pl_augmented_worker.sh`
- `scripts/preflight_credentials.sh`
- `scripts/cosmos_worker.sh`
- `scripts/stage_run_artifacts.sh`
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
