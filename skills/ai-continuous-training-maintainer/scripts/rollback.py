"""Restore files from a snapshot backup."""
import hashlib
import json
import sys
from pathlib import Path


def verify_snapshot(snapshot_path: Path) -> bool:
    snap = json.loads(snapshot_path.read_text(encoding="utf-8"))
    for filepath, expected_hash in snap.items():
        fp = Path(filepath)
        if not fp.is_file():
            print(f"MISSING: {filepath}")
            return False
        actual = hashlib.sha256(fp.read_bytes()).hexdigest()
        if actual != expected_hash:
            print(f"MODIFIED: {filepath} (expected {expected_hash}, got {actual})")
            return False
    print("All files match snapshot.")
    return True


if __name__ == "__main__":
    snapshot_path = Path(sys.argv[1])
    verify_snapshot(snapshot_path)
