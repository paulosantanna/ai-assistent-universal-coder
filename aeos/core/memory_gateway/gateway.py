"""AEOS Memory Gateway — resolves memory references for agents."""

from pathlib import Path
from typing import Any


class MemoryGateway:
    def __init__(self, memory_dir: str | Path):
        self.memory_dir = Path(memory_dir)

    def query_refs(self, scope: dict) -> list[dict]:
        refs = []
        if not self.memory_dir.exists():
            return refs
        for f in self.memory_dir.glob("*.md"):
            refs.append({"type": "memory_file", "path": str(f), "name": f.stem})
        return refs

    def read(self, ref: str) -> str | None:
        path = self.memory_dir / f"{ref}.md"
        if path.exists():
            return path.read_text(encoding="utf-8")
        return None