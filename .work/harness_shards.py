"""Split harness-eval decks (Track B claims.md, Track C surfaces.md) into shuffled shards for blind judges.

Shuffle is seeded so plants (P00x / S9xx) are spread across shards instead of clustering in the last one.
Judges still see every ID exactly once overall; merge_* scripts get one concatenated table per judge.
"""
import pathlib
import random
import re
import sys

RUN = pathlib.Path(sys.argv[1])
N_B, N_C, SEED = 4, 4, 20261120
OUT = RUN / "shards"
OUT.mkdir(exist_ok=True)


def split_b():
    text = (RUN / "claims.md").read_text(encoding="utf-8")
    head, _, table = text.partition("## Claims")
    rows = [l for l in table.splitlines() if re.match(r"^\|\s*[CP]\d+\s*\|", l)]
    random.Random(SEED).shuffle(rows)
    size = -(-len(rows) // N_B)
    for k in range(N_B):
        chunk = rows[k * size : (k + 1) * size]
        body = (head + "## Claims\n\n| ID | Tier | Source | Quote |\n|----|------|--------|-------|\n" + "\n".join(chunk) + "\n")
        (OUT / f"B-{k}.md").write_text(body, encoding="utf-8", newline="\n")
        (OUT / f"B-{k}.ids.txt").write_text("\n".join(re.match(r"^\|\s*([CP]\d+)", r).group(1) for r in chunk), encoding="utf-8")
    print("B rows", len(rows), "shards", N_B, "size~", size)


def split_c():
    text = (RUN / "surfaces.md").read_text(encoding="utf-8")
    head, _, rest = text.partition("## Surfaces")
    blocks = re.split(r"(?m)^(?=### S\d+ \|)", rest)
    blocks = [b for b in blocks if b.startswith("### S")]
    random.Random(SEED).shuffle(blocks)
    size = -(-len(blocks) // N_C)
    for k in range(N_C):
        chunk = blocks[k * size : (k + 1) * size]
        (OUT / f"C-{k}.md").write_text(head + "## Surfaces\n\n" + "\n".join(chunk), encoding="utf-8", newline="\n")
        (OUT / f"C-{k}.ids.txt").write_text("\n".join(re.match(r"### (S\d+)", b).group(1) for b in chunk), encoding="utf-8")
    print("C surfaces", len(blocks), "shards", N_C, "size~", size)


split_b()
split_c()
