---
name: security-ownership-map
description: "Assimilated OpenAI/TLC git ownership topology skill. Build people-to-file maps, bus factor and sensitive-code ownership from git history. Triggers: security ownership, bus factor, orphaned sensitive code, CODEOWNERS reality check. Do not use for general maintainer lists or threat modeling (security-threat-model)."
---

# Security Ownership Map

Assimilated from installed `security-ownership-map` 1.0.0. Original contract: `references/ORIGINAL_SKILL.md`. Scripts: `scripts/run_ownership_map.py`, `scripts/query_ownership.py`.

## Identity

A skill of the single canonical `codenavi-agent`. It creates no new agent identity.

## Mission

From git history, build a bipartite people/file graph, compute ownership risk and optional co-change clusters, export CSV/JSON (and optional GraphML) for review or Neo4j.

## Activation

- User explicitly wants a security-oriented ownership or bus-factor analysis grounded in git history.

## Non-activation

- General "who maintains this" without security risk.
- Threat modeling (`security-threat-model`).
- Language best-practice review (`security-best-practices`).

## Critical rules

1. Resolve `<skill-dir>` as the directory that contains this `SKILL.md`. Run `python`/`py -3` as `<skill-dir>/scripts/run_ownership_map.py` with `--repo` and `--out`. Do not run `python skills/skills/...` from the original examples.
2. `networkx` is required. Check the environment/lockfile before installing. Do not add it silently to this AEOS repo unless the user asked to persist that dependency.
3. Default author identity, author date, exclude merges and Dependabot unless overridden.
4. Write outputs to an untracked or user-named directory. Do not commit personal emails or raw identity dumps into MEMORY or tracked reports without redaction.
5. Follow flags, sensitivity rules and Neo4j notes in `references/ORIGINAL_SKILL.md` and `references/neo4j-import.md`.
6. Query slices with `scripts/query_ownership.py`.

## Continuity

Promote only verified durable ownership decisions (CODEOWNERS gaps that were confirmed) into `.notebook/MEMORY.md`. Never persist author emails as secrets-adjacent PII in notebook.
