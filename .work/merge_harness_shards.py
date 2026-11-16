"""Concatenate judge shard score tables into the merge_* input filenames."""
from __future__ import annotations

import pathlib
import re

RUN = pathlib.Path(__file__).resolve().parents[1] / ".harness-eval/runs/2026-11-16-abc"
SH = RUN / "shards"
ID_RE = re.compile(r"^\|\s*([CPS]\d+)\s*\|")
MODEL_RE = re.compile(r"model:\s*`?([^\n`]+)`?", re.I)
HEADER_RE = re.compile(r"^\|\s*ID\s*\|", re.I)


def write_table(pattern: str, out_name: str, title: str) -> None:
    paths = sorted(SH.glob(pattern))
    if not paths:
        raise SystemExit(f"no shards for {pattern}")
    rows: list[str] = []
    header = None
    sep = None
    models: set[str] = set()
    for path in paths:
        text = path.read_text(encoding="utf-8")
        m = MODEL_RE.search(text)
        if m:
            models.add(m.group(1).strip())
        for line in text.splitlines():
            if header is None and HEADER_RE.match(line):
                header = line
            elif sep is None and line.startswith("|") and set(line.replace("|", "").replace("-", "").replace(" ", "").replace(":", "")) == set():
                sep = line
            elif ID_RE.match(line):
                rows.append(line)
    seen: set[str] = set()
    uniq: list[str] = []
    for row in rows:
        cid = ID_RE.match(row).group(1)
        if cid in seen:
            continue
        seen.add(cid)
        uniq.append(row)
    if header is None or sep is None:
        raise SystemExit(f"missing header/sep for {pattern}")
    model_s = "|".join(sorted(models)) or "unrecorded"
    lines = [
        f"# {title}",
        "",
        f"> model: `{model_s}`",
        f"> shards: {len(paths)} · rows: {len(uniq)}",
        "",
        "## Scores",
        "",
        header,
        sep,
        *uniq,
        "",
    ]
    out = RUN / out_name
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(out_name, "rows", len(uniq), "models", model_s)


write_table("05-j1-*.md", "05-redundancy-j1.md", "Harness Eval: Redundancy Judge1 (Track B)")
write_table("06-j2-*.md", "06-blind-scores.md", "Harness Eval: Redundancy Judge2 Blind (Track B)")
write_table("08-j1-*.md", "08-usefulness-j1.md", "Harness Eval: Usefulness Judge1 (Track C)")
write_table("09-j2-*.md", "09-usefulness-j2.md", "Harness Eval: Usefulness Judge2 (Track C)")
