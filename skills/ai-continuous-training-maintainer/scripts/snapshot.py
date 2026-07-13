"""Create SHA-256 snapshots of files for rollback."""
import hashlib
import json
import sys
from pathlib import Path


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot(files: list[Path], output: Path) -> dict:
    snap = {}
    for fp in files:
        if fp.is_file():
            snap[str(fp)] = sha256_file(fp)
    output.write_text(
        json.dumps(snap, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return snap


if __name__ == "__main__":
    files = [Path(p) for p in sys.argv[1:-1]]
    output = Path(sys.argv[-1])
    snapshot(files, output)
    print(f"Snapshot saved to {output}")
