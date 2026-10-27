# Skill provenance

Updated: 2026-10-26
Owner: codenavi-agent
Entry point: ../SKILL.md.

Source: [tlc-spec-driven 4.0.0](https://github.com/tech-leads-club/agent-skills/tree/ef2672d67adebb1fc95af83e25fcba4d8cce02a7/packages/skills-catalog/skills/(development)/tlc-spec-driven), commit `ef2672d67adebb1fc95af83e25fcba4d8cce02a7`.
Author: Felipe Rodrigues - github.com/felipfr. License: CC-BY-4.0, retained in `00_skills/TLC-LICENSE`.
Official resource hashes and Git executable flags: `00_skills/upstream.manifest.json`, entry `tlc-spec-driven`. Source contract and resources are retained under `tlc/`.

Local adaptation: <=100-line entry, explicit resource paths, session authorization, one codenavi-agent identity and sequential self-verification. Source claims of independent sub-agents do not apply locally. No runtime dependencies or providers are installed.

The requested versions are pinned intentionally; newer upstream releases are not implicitly installed. Missing tools or evidence must be reported.

Executable local helpers are under `../scripts/`. `mutate.py` registers only signals supported by the platform and uses taskkill /T /F on Windows to stop a timed-out proof tree. Official snapshots are unchanged. Source bug reproduced by selftest on Windows before this patch.
Python references: https://docs.python.org/3/library/signal.html and https://docs.python.org/3/library/subprocess.html.
