# Defects and adaptation

## Contents

- Findings
- Evidence
- Grade

## Findings

- Original `SKILL.md` has 204 physical lines. The TLC cap is 100, so the operational body moved to `references/procedure.md`.
- Original frontmatter keys: name, version, description, license, compatibility, metadata, allowed-tools.
- Original description had no `Do NOT use` boundary in the routing line.
- Upstream autonomy says to execute after analysis and to ask only for keys, deletion, or ties. TLC gates keep read-only detection and require confirmation before deploy, shutdown, and deletion.
- The Claude-style allowed-tools allowlist and the OpenAPI schema paths were not copied; they are not a permission grant in this workspace.

## Evidence

- Entrypoint pattern hits:
- L35: `allowed-tools: Bash(echo *) Bash(nvidia-smi *) Bash(curl --version *) Bash(docker ps *) Bash(docker info *) Bash(docker --version *) Bash(docker version *) Bash(docker logs *) Bash`
- Sample of relative links that do not resolve inside the upstream package (0 total):
- None in the copied markdown set.
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
