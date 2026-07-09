from __future__ import annotations

import zipfile
import io

from aeos.core.tool_router.adapters.package_local_adapter import PackageLocalAdapter


class TestPackageLocalAdapter:
    def setup_method(self):
        self.adapter = PackageLocalAdapter()

    def _make_zip(self, entries: dict[str, str]) -> bytes:
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            for name, content in entries.items():
                zf.writestr(name, content)
        buf.seek(0)
        return buf.read()

    def test_verify_clean_zip(self):
        data = self._make_zip({"safe.txt": "hello"})
        result = self.adapter.execute("package.verify", "", {"content": list(data)})
        assert result["verified"] is True

    def test_block_path_traversal(self):
        data = self._make_zip({"../../etc/passwd": "evil"})
        result = self.adapter.execute("package.verify", "", {"content": list(data)})
        assert result["verified"] is False
        assert any("traversal" in e.lower() for e in result.get("errors", []))

    def test_block_absolute_path(self):
        data = self._make_zip({"/absolute/file.txt": "data"})
        result = self.adapter.execute("package.verify", "", {"content": list(data)})
        assert result["verified"] is False
        assert any("absolute" in e.lower() for e in result.get("errors", []))

    def test_block_git_dir(self):
        data = self._make_zip({".git/config": "dummy"})
        result = self.adapter.execute("package.verify", "", {"content": list(data)})
        assert result["verified"] is False
        assert any(".git" in e for e in result.get("errors", []))

    def test_block_secret_file_name(self):
        data = self._make_zip({".env": "SECRET=value"})
        result = self.adapter.execute("package.verify", "", {"content": list(data)})
        assert result["verified"] is False
        assert any("secret" in e.lower() for e in result.get("errors", []))

    def test_invalid_zip(self):
        result = self.adapter.execute("package.verify", "", {"content": list(b"not a zip")})
        assert result["verified"] is False

    def test_inspect_manifest(self):
        data = self._make_zip({"file1.txt": "a", "dir/file2.txt": "b"})
        with open("_test_pkg.zip", "wb") as f:
            f.write(data)
        result = self.adapter.execute("package.inspect", "_test_pkg.zip", {})
        import os; os.remove("_test_pkg.zip")
        assert "entries" in result
        assert result["count"] == 2
