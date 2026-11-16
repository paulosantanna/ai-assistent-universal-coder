# Skill provenance

Updated: 2026-10-26
Owner: codenavi-agent
Entry point: ../SKILL.md.

Source: [tlc-spec-lean 2.0.0](https://github.com/tech-leads-club/agent-skills/tree/2fca1d19753fa8ec2a3449371b97e4830544461a/packages/skills-catalog/skills/(development)/tlc-spec-lean), commit `2fca1d19753fa8ec2a3449371b97e4830544461a`.
Author: Tech Leads Club - github.com/tech-leads-club. License: CC-BY-4.0, retained in `00_skills/TLC-LICENSE`.
Official resource hashes and Git executable flags: `00_skills/upstream.manifest.json`, entry `tlc-spec-lean`. Source contract and resources are retained under `../../tlc-spec-lean/references/tlc/`.

Local adaptation: <=100-line entry, explicit resource paths, session authorization, one codenavi-agent identity and sequential self-verification. Source claims of independent sub-agents do not apply locally. No runtime dependencies or providers are installed.
Direct Python/reference copies follow the same pinned source; legacy Node entrypoints forward to the Python gates.

The requested versions are pinned intentionally; newer upstream releases are not implicitly installed. Missing tools or evidence must be reported.

Executable local helpers are under `../scripts/`. `mutate.py` registers only signals supported by the platform and uses taskkill /T /F on Windows to stop a timed-out proof tree. Official snapshots are unchanged. Source bug reproduced by selftest on Windows before this patch.
Python references: https://docs.python.org/3/library/signal.html and https://docs.python.org/3/library/subprocess.html.
