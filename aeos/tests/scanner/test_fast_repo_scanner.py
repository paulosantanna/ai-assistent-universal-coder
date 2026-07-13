import pytest
from pathlib import Path

from aeos.core.scanner.fast_repo_scanner import FastRepoScanner


def test_scan_counts_python_files(tmp_path: Path):
    (tmp_path / "main.py").write_text("x = 1")
    (tmp_path / "utils.py").write_text("y = 2")
    (tmp_path / "README.md").write_text("# docs")
    stats = FastRepoScanner(root=tmp_path, exclude=[]).scan()
    assert stats.total_files == 3
    assert stats.scanned_files == 3
    assert stats.python_files == 2
    assert stats.config_files == 0
    assert stats.ignored_files == 0


def test_scan_excludes_directory(tmp_path: Path):
    (tmp_path / "main.py").write_text("x = 1")
    venv = tmp_path / ".venv" / "Lib"
    venv.mkdir(parents=True)
    (venv / "os.py").write_text("import os")
    stats = FastRepoScanner(root=tmp_path, exclude=[".venv"]).scan()
    assert stats.total_files == 2
    assert stats.scanned_files == 1
    assert stats.ignored_files == 1
    assert stats.python_files == 1


def test_scan_excludes_multiple_patterns(tmp_path: Path):
    (tmp_path / "main.py").write_text("x = 1")
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "HEAD").write_text("ref")
    pc_dir = tmp_path / "__pycache__"
    pc_dir.mkdir()
    (pc_dir / "foo.cpython.py").write_text("code")
    nm_dir = tmp_path / "node_modules"
    nm_dir.mkdir()
    (nm_dir / "index.js").write_text("js")
    stats = FastRepoScanner(root=tmp_path, exclude=[".git", "__pycache__", "node_modules"]).scan()
    assert stats.total_files == 4
    assert stats.scanned_files == 1
    assert stats.ignored_files == 3
    assert stats.python_files == 1


def test_scan_counts_config_files(tmp_path: Path):
    (tmp_path / "cfg.yaml").write_text("key: val")
    (tmp_path / "cfg.yml").write_text("key: val")
    (tmp_path / "cfg.json").write_text('{"key": "val"}')
    (tmp_path / "main.py").write_text("x = 1")
    stats = FastRepoScanner(root=tmp_path, exclude=[]).scan()
    assert stats.config_files == 3
    assert stats.python_files == 1


def test_scan_metadata_only_large_file(tmp_path: Path):
    (tmp_path / "small.py").write_text("x = 1")
    large = tmp_path / "large.bin"
    with large.open("wb") as f:
        f.write(b"x" * (11 * 1024 * 1024))
    stats = FastRepoScanner(root=tmp_path, exclude=[], max_file_mb=10).scan()
    assert stats.total_files == 2
    assert stats.scanned_files == 2
    assert stats.metadata_only_files == 1
    assert stats.metadata_only_bytes >= 11 * 1024 * 1024


def test_scan_respects_gitignore(tmp_path: Path):
    (tmp_path / ".gitignore").write_text("*.log\ncache/")
    (tmp_path / "main.py").write_text("x = 1")
    (tmp_path / "app.log").write_text("error")
    cache = tmp_path / "cache"
    cache.mkdir()
    (cache / "data.txt").write_text("data")
    stats = FastRepoScanner(root=tmp_path, exclude=[], respect_gitignore=True).scan()
    assert stats.total_files == 4
    assert stats.scanned_files == 2
    assert stats.ignored_files == 2
    assert stats.python_files == 1


def test_scan_heaviest_dirs(tmp_path: Path):
    sub = tmp_path / "heavy"
    sub.mkdir()
    for i in range(3):
        (sub / f"file{i}.py").write_text("x" * 1000)
    (tmp_path / "light.py").write_text("x = 1")
    stats = FastRepoScanner(root=tmp_path, exclude=[]).scan()
    top = stats.top_20_dirs
    assert any("heavy" in d for d, _, _ in top)


def test_scan_inflated_detection(tmp_path: Path):
    for i in range(250):
        (tmp_path / f"file{i}.py").write_text("x")
    stats = FastRepoScanner(root=tmp_path, exclude=[]).scan()
    stats.total_files = 250_000
    stats.scanned_files = 250_000
    assert stats.inflated is True


def test_scan_not_inflated_small(tmp_path: Path):
    (tmp_path / "main.py").write_text("x = 1")
    stats = FastRepoScanner(root=tmp_path, exclude=[]).scan()
    assert stats.inflated is False


def test_scan_ignored_dirs_tracked(tmp_path: Path):
    node = tmp_path / "node_modules" / "pkg"
    node.mkdir(parents=True)
    (node / "index.js").write_text("js")
    stats = FastRepoScanner(root=tmp_path, exclude=["node_modules"]).scan()
    assert "node_modules" in stats.ignored_dirs


def test_scan_all_skip_no_pass(tmp_path: Path):
    (tmp_path / "ignored.py").write_text("x = 1")
    stats = FastRepoScanner(root=tmp_path, exclude=["*.py"]).scan()
    assert stats.scanned_files == 0
    assert stats.python_files == 0


def test_scan_default_exclusions(tmp_path: Path):
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "HEAD").write_text("ref")
    pc_dir = tmp_path / "__pycache__"
    pc_dir.mkdir()
    (pc_dir / "c.py").write_text("code")
    (tmp_path / "main.py").write_text("x = 1")
    stats = FastRepoScanner(root=tmp_path).scan()
    assert stats.total_files == 3
    assert stats.scanned_files == 1
    assert stats.python_files == 1
    assert stats.ignored_files == 2


def test_scan_can_prune_ignored_dirs_without_counting_files(tmp_path: Path):
    node = tmp_path / "node_modules" / "pkg"
    node.mkdir(parents=True)
    for i in range(20):
        (node / f"file{i}.js").write_text("js")
    (tmp_path / "main.py").write_text("x = 1")

    stats = FastRepoScanner(root=tmp_path, exclude=["node_modules"], count_ignored_files=False).scan()

    assert stats.total_files == 1
    assert stats.ignored_files == 0
    assert stats.scanned_files == 1
    assert "node_modules" in stats.ignored_dirs
