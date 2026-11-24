# always-on agents

Updated: 2026-11-24
Entry point: `00_skills/(tooling)/always-on-agents/SKILL.md`

- Workers are host CLI processes of `codenavi-agent`, born for one generation and dead after it. Resume is refused.
- Cursor argv is `agent -p ... --model`. OpenCode argv is `opencode run --model` without `--continue` or `--session`. Ollama is refused.
- Grok and GLM are paid from published prices. A paid generation is three processes and the approval is single-use. `scripts/free-models.json` starts empty; a priced marker beats the list.
- `python scripts/run_tests.py`: 27 tests, exit 0. `python quality/validate.py`: PASS, 325 skills, one changed skill assessed.
- `agent` and `opencode` were absent on this machine on 2026-11-24, so no live paid worker ran.
