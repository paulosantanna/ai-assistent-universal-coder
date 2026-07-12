from __future__ import annotations

from pathlib import Path

import pytest

from aeos_lsp.workspace.manager import WorkspaceManager
from aeos_lsp.workspace.cache import DocumentCache
from aeos_lsp.workspace.folders import WorkspaceFolderInfo, detect_aeos_root, validate_folder


class TestWorkspaceManager:
    @pytest.fixture
    def manager(self) -> WorkspaceManager:
        return WorkspaceManager()

    def test_initial_state(self, manager):
        assert manager.root_uri is None
        assert len(manager.workspace_folders) == 0

    def test_add_folder(self, manager):
        folder = WorkspaceFolderInfo(uri="file:///workspace/subdir", name="subdir")
        manager.add_folder(folder)
        assert len(manager.workspace_folders) == 1

    def test_get_folder(self, manager):
        folder = WorkspaceFolderInfo(uri="file:///workspace/test", name="test")
        manager.add_folder(folder)
        retrieved = manager.get_folder("file:///workspace/test")
        assert retrieved is folder

    def test_remove_folder(self, manager):
        folder = WorkspaceFolderInfo(uri="file:///workspace/to-remove", name="to-remove")
        manager.add_folder(folder)
        assert manager.remove_folder("file:///workspace/to-remove")
        assert len(manager.workspace_folders) == 0

    def test_update_folders(self, manager):
        added = [
            WorkspaceFolderInfo(uri="file:///workspace/a", name="a"),
            WorkspaceFolderInfo(uri="file:///workspace/b", name="b"),
        ]
        manager.update_folders(added, [])
        assert len(manager.workspace_folders) == 2

    def test_is_trusted_default(self, manager):
        assert not manager.is_trusted()

    def test_set_trusted(self, manager):
        manager.set_trusted(True)
        assert manager.is_trusted()


class TestDocumentCache:
    @pytest.fixture
    def cache(self) -> DocumentCache:
        return DocumentCache(max_size_mb=1)

    def test_set_and_get(self, cache):
        cache.set("uri1", "content1", size_bytes=10)
        assert cache.get("uri1") == "content1"

    def test_get_nonexistent(self, cache):
        assert cache.get("nonexistent") is None

    def test_delete(self, cache):
        cache.set("to_delete", "content", size_bytes=10)
        assert cache.delete("to_delete")
        assert cache.get("to_delete") is None

    def test_clear(self, cache):
        cache.set("a", "1", size_bytes=10)
        cache.clear()
        assert cache.get("a") is None

    def test_stats(self, cache):
        cache.set("a", "val", size_bytes=10)
        stats = cache.stats()
        assert stats["count"] >= 1

    def test_hit_counting(self, cache):
        cache.set("hit", "value", size_bytes=10)
        cache.get("hit")
        stats = cache.stats()
        assert stats["hits"] == 1
        assert stats["misses"] == 0

    def test_miss_counting(self, cache):
        cache.get("miss")
        stats = cache.stats()
        assert stats["misses"] == 1

    def test_count_property(self, cache):
        cache.set("a", "1", size_bytes=10)
        assert cache.count == 1

    def test_size_bytes_property(self, cache):
        cache.set("a", "val", size_bytes=50)
        assert cache.size_bytes >= 50


class TestWorkspaceFolderInfo:
    def test_folder_creation(self):
        folder = WorkspaceFolderInfo(uri="file:///workspace/test", name="test")
        assert folder.uri == "file:///workspace/test"
        assert not folder.trusted

    def test_detect_aeos_root_found(self, temp_dir):
        config = temp_dir / "aeos.config.yaml"
        config.write_text("aeos:\n  name: test\n", encoding="utf-8")
        root = detect_aeos_root(temp_dir)
        assert root is not None

    def test_detect_aeos_root_not_found(self, temp_dir):
        root = detect_aeos_root(temp_dir)
        assert root is None

    def test_validate_folder(self, temp_dir):
        valid, msg = validate_folder(temp_dir)
        assert valid
        assert msg is None
