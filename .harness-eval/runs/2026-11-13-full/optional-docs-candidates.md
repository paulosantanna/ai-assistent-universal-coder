# Optional docs (not in eval unless approved)

Non-agent documents cited by T0/T1. **ADRs / RFCs are always excluded.**
Agent skill-tree files (`.agents/skills`, `.cursor/skills`, `.claude/skills`) are always in scope.

## Ask the user

Present the doc **types** below and ask which (if any) to include in this run.
Then re-run inventory with `--include-doc-type <type>` and/or `--include-doc <path>`.

## Always excluded (decision records)

_1 path(s) skipped (ADR/RFC trees or filenames)._
- `00_skills/(architecture)/architecture-decision-record/SKILL.md`

## Optional types (default: omitted)

| Type | Count | Example paths |
|------|------:|---------------|
| `.notebook` | 5 | `.notebook/HANDOFF.md`, `.notebook/INDEX.md`, `.notebook/LEARNING.md` (+2) |
| `00_skills` | 304 | `00_skills/(architecture)/ai-architecture-expert/SKILL.md`, `00_skills/(architecture)/angular-8-to-20-migration/SKILL.md`, `00_skills/(architecture)/architecture-decision-log/SKILL.md` (+301) |

### Re-run examples

```bash
python3 "$SKILL_DIR/scripts/inventory_extract.py" --root . --run-id "$RUN_ID" \
  --include-doc-type docs
python3 "$SKILL_DIR/scripts/inventory_extract.py" --root . --run-id "$RUN_ID" \
  --include-doc docs/context.md --include-doc docs/infrastructure.md
```

## Included optional docs this run

_None (default)._

