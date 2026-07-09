from __future__ import annotations

import tempfile
from pathlib import Path

from aeos.core.tool_router.adapters.filesystem_readonly_adapter import FilesystemReadonlyAdapter
from aeos.core.tool_router.adapters.filesystem_sandbox_write_adapter import FilesystemSandboxWriteAdapter


class TestFilesystemReadonlyAdapter:
    def setup_method(self):
        self.adapter = FilesystemReadonlyAdapter()

    def test_list_dir_returns_entries(self):
        result = self.adapter.execute("filesystem.list", "aeos/config", {})
        assert "entries" in result
        assert result["count"] > 0

    def test_read_text_file(self):
        result = self.adapter.execute("filesystem.read", "aeos/config/aeos.config.yaml", {})
        assert "content" in result
        assert result["size"] > 0

    def test_read_nonexistent_file(self):
        result = self.adapter.execute("filesystem.read", "nonexistent.txt", {})
        assert "error" in result

    def test_stat_exists(self):
        result = self.adapter.execute("filesystem.exists", "aeos/config", {})
        assert result["exists"] is True

    def test_stat_nonexistent(self):
        result = self.adapter.execute("filesystem.exists", "nonexistent_path", {})
        assert result["exists"] is False

    def test_unknown_action(self):
        result = self.adapter.execute("invalid.action", "", {})
        assert "error" in result

    def test_read_exceeds_limit(self):
        tiny = FilesystemReadonlyAdapter(max_file_bytes=10)
        result = tiny.execute("filesystem.read", "aeos/config/aeos.config.yaml", {})
        assert "error" in result
        assert "exceeds size limit" in result["error"]


class TestFilesystemSandboxWriteAdapter:
    def setup_method(self):
        self.sandbox = Path(".aeos/sandbox")
        self.adapter = FilesystemSandboxWriteAdapter(sandbox_base=str(self.sandbox))

    def test_write_allowed_in_sandbox(self):
        result = self.adapter.execute("filesystem.write_sandbox", "test_file.txt", {"content": "hello"})
        assert result.get("written") is True
        assert (self.sandbox / "test_file.txt").exists()

    def test_block_outside_sandbox_relative(self):
        result = self.adapter.execute("filesystem.write_sandbox", "../outside.txt", {"content": "blocked"})
        assert "outside sandbox" in (result.get("error", "") or "").lower()

    def test_block_absolute_path(self):
        result = self.adapter.execute("filesystem.write_sandbox", "/etc/passwd", {"content": "blocked"})
        assert "error" in result

    def test_block_path_traversal(self):
        result = self.adapter.execute("filesystem.write_sandbox", "good/../../evil.txt", {"content": "blocked"})
        assert "error" in result

    def test_mkdir_allowed(self):
        result = self.adapter.execute("filesystem.mkdir_sandbox", "new_dir", {})
        assert result.get("created") is True
        assert (self.sandbox / "new_dir").exists()

    def test_unknown_action(self):
        result = self.adapter.execute("invalid.action", "", {})
        assert "error" in result
