"""Rewrite citations of the phantom root `AGENT.md` to the real root contract `AGENTS.md`.

Only lines classified as root_phantom by agentmd_audit.py (plus 4 explicit root cites found by hand)
are touched. Subtree AGENT.md contracts and per-skill AGENT.md package layers are different concepts.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
audit = json.loads((ROOT / ".work" / "agentmd_audit.json").read_text(encoding="utf-8"))

# The restored standard describes the historical removal of root AGENT.md on purpose.
KEEP_AS_HISTORY = {"references/CODENAVI_FULL_WORKSPACE_STANDARD.md"}

# (file, 1-based line) -> exact old -> new for root cites the pattern classifier does not match.
EXPLICIT = {
    ("docs/WORKSPACE_GUIDE.md", 11): ("inherits `AGENT.md`", "inherits `AGENTS.md`"),
    ("docs/WORKSPACE_GUIDE.md", 17): ("— `AGENT.md`, policies", "— `AGENTS.md`, policies"),
    ("docs/WORKSPACE_GUIDE.md", 44): ("root `AGENT.md`/`AGENTS.md`", "root `AGENTS.md`"),
    ("docs/GOVERNANCE_COVERAGE.md", 22): ("AGENT.md", "AGENTS.md"),
}
PATTERNS = [re.compile(p) for p in (
    r"root `AGENT\.md`", r"Read `AGENT\.md`", r"herda `AGENT\.md`",
    r"Agent único: `AGENT\.md`", r"definido em `AGENT\.md`", r"governed by the root `AGENT\.md`",
)]

targets: dict[str, set[int]] = {}
for x in audit["root_phantom"]:
    if x["file"] not in KEEP_AS_HISTORY:
        targets.setdefault(x["file"], set()).add(x["line"])
for (f, n) in EXPLICIT:
    targets.setdefault(f, set()).add(n)

changed = 0
for rel, lines in sorted(targets.items()):
    path = ROOT / rel
    with open(path, encoding="utf-8", newline="") as fh:
        raw = fh.read()
    parts = raw.split("\n")
    for n in sorted(lines):
        old_line = parts[n - 1]
        if (rel, n) in EXPLICIT:
            old, new = EXPLICIT[(rel, n)]
            assert old in old_line, (rel, n, old_line)
            new_line = old_line.replace(old, new, 1)
        else:
            new_line = old_line
            for p in PATTERNS:
                new_line = p.sub(lambda m: m.group(0).replace("AGENT.md", "AGENTS.md"), new_line)
        assert new_line != old_line, (rel, n, old_line)
        parts[n - 1] = new_line
        changed += 1
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(parts))
print("files:", len(targets), "lines changed:", changed)
