"""Fast repo scanner with exclusion support and stats tracking."""

import time
from pathlib import Path
from collections import defaultdict

from aeos.core.scanner.exclusions import (
    DEFAULT_EXCLUDE_PATTERNS,
    normalize_patterns,
    collect_gitignore_patterns,
    is_excluded,
)


class ScanStats:
    def __init__(self):
        self.total_files = 0
        self.total_bytes = 0
        self.ignored_files = 0
        self.ignored_dirs = set()
        self.scanned_files = 0
        self.scanned_bytes = 0
        self.metadata_only_files = 0
        self.metadata_only_bytes = 0
        self.python_files = 0
        self.config_files = 0
        self.elapsed_seconds = 0.0
        self.heaviest_dirs: list[tuple[str, int, int]] = []

    @property
    def dir_count_by_size(self) -> list[tuple[str, int, int]]:
        return sorted(self.heaviest_dirs, key=lambda x: -x[2])

    @property
    def top_20_dirs(self) -> list[tuple[str, int, int]]:
        return self.dir_count_by_size[:20]

    @property
    def inflated(self) -> bool:
        if self.elapsed_seconds <= 0:
            return False
        return self.scanned_files > 200_000 or self.scanned_bytes > 500_000_000

    def __repr__(self) -> str:
        return (
            f"ScanStats(total={self.total_files}, scanned={self.scanned_files}, "
            f"ignored_files={self.ignored_files}, ignored_dirs={len(self.ignored_dirs)}, "
            f"python={self.python_files}, config={self.config_files}, "
            f"bytes={self.scanned_bytes}, elapsed={self.elapsed_seconds:.2f}s, "
            f"inflated={self.inflated})"
        )


class FastRepoScanner:
    def __init__(
        self,
        root: str | Path,
        exclude: list[str] | None = None,
        max_file_mb: int = 10,
        metadata_only_large_files: bool = False,
        respect_gitignore: bool = False,
    ):
        self.root = Path(root).resolve()
        patterns = list(exclude or DEFAULT_EXCLUDE_PATTERNS)
        if respect_gitignore:
            patterns.extend(collect_gitignore_patterns(self.root))
        self.exclude_patterns = normalize_patterns(patterns)
        self.max_file_bytes = max_file_mb * 1024 * 1024
        self.metadata_only_large_files = metadata_only_large_files

    def scan(self) -> ScanStats:
        stats = ScanStats()
        start = time.perf_counter()
        dir_tracker: dict[str, list[int]] = defaultdict(lambda: [0, 0])

        for path in self.root.rglob("*"):
            if path.is_dir():
                continue
            stats.total_files += 1
            try:
                file_size = path.stat().st_size
            except OSError:
                file_size = 0
            stats.total_bytes += file_size

            if is_excluded(path, self.root, self.exclude_patterns):
                stats.ignored_files += 1
                for parent in path.relative_to(self.root).parents:
                    p = str(parent)
                    if p == ".":
                        break
                    stats.ignored_dirs.add(p)
                continue

            stats.scanned_files += 1
            stats.scanned_bytes += file_size

            if path.suffix == ".py":
                stats.python_files += 1
            if path.suffix in (".yaml", ".yml", ".json"):
                stats.config_files += 1

            if file_size > self.max_file_bytes:
                stats.metadata_only_files += 1
                stats.metadata_only_bytes += file_size

            rel_parent = str(path.relative_to(self.root).parent)
            if rel_parent == ".":
                rel_parent = "(root)"
            dir_tracker[rel_parent][0] += 1
            dir_tracker[rel_parent][1] += file_size

        stats.heaviest_dirs = [
            (d, c, b) for d, (c, b) in dir_tracker.items()
        ]
        stats.elapsed_seconds = time.perf_counter() - start
        return stats
