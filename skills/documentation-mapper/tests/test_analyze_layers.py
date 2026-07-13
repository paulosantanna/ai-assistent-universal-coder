#!/usr/bin/env python3
"""Tests for the 10-layer analysis script."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from analyze_layers import (
    analyze_infrastructure,
    analyze_data_persistence,
    analyze_backend_api,
    analyze_frontend,
    analyze_business_logic,
    analyze_integrations,
    analyze_security,
    analyze_devops,
    analyze_observability,
    analyze_governance,
    find_files,
    read_preview
)


class TestFindFiles(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        (self.test_dir / "Dockerfile").write_text("FROM node:18")
        (self.test_dir / "src").mkdir()
        (self.test_dir / "src" / "routes").mkdir()
        (self.test_dir / "src" / "routes" / "api.ts").write_text("router.get('/api/users', ...)")
        (self.test_dir / "node_modules").mkdir()
        (self.test_dir / "node_modules" / "fake.ts").write_text("should be excluded")

    def test_find_dockerfile(self):
        files = find_files(self.test_dir, ["Dockerfile"])
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].name, "Dockerfile")

    def test_find_route_files(self):
        files = find_files(self.test_dir, ["**/*route*", "**/routes/**"])
        self.assertGreaterEqual(len(files), 1)

    def test_node_modules_excluded(self):
        files = find_files(self.test_dir, ["**/*.ts"])
        self.assertFalse(any("node_modules" in str(f) for f in files))

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)


class TestReadPreview(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.small_file = self.test_dir / "small.txt"
        self.small_file.write_text("Hello World")
        self.large_file = self.test_dir / "large.txt"
        self.large_file.write_text("A" * 1000)
        self.binary_file = self.test_dir / "binary.bin"
        self.binary_file.write_bytes(b"\x00\x01\x02")

    def test_small_file(self):
        result = read_preview(self.small_file)
        self.assertEqual(result, "Hello World")

    def test_large_file_truncated(self):
        result = read_preview(self.large_file, max_chars=100)
        self.assertIn("[TRUNCATED]", result)
        self.assertLessEqual(len(result), 100 + 20)  # allow buffer for truncation marker

    def test_binary_file(self):
        result = read_preview(self.binary_file)
        self.assertIn("ERROR", result)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)


class TestAnalyzers(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        (self.test_dir / "Dockerfile").write_text("FROM node:18\nWORKDIR /app\nCOPY . .\nCMD npm start")
        (self.test_dir / "docker-compose.yml").write_text("version: '3'\nservices:\n  app:\n    build: .")
        (self.test_dir / "src").mkdir()
        (self.test_dir / "src" / "schema.ts").write_text("const UserSchema = new Schema({ name: String, email: { type: String, required: true } })")
        (self.test_dir / "src" / "routes").mkdir()
        (self.test_dir / "src" / "routes" / "user.ts").write_text("router.get('/api/users', list)")
        (self.test_dir / "package.json").write_text(json.dumps({
            "dependencies": { "express": "^4.18", "react": "^18.2", "mongoose": "^7.0" },
            "devDependencies": { "jest": "^29.0" }
        }))
        (self.test_dir / "src" / "App.tsx").write_text("export default function App() { return <div>Hello</div> }")
        (self.test_dir / "src" / "services").mkdir()
        (self.test_dir / "src" / "services" / "auth.ts").write_text("export function login(email, password) { ... }")
        (self.test_dir / ".github").mkdir()
        (self.test_dir / ".github" / "workflows").mkdir()
        (self.test_dir / ".github" / "workflows" / "ci.yml").write_text("name: CI\non: push\njobs:\n  test:\n    runs-on: ubuntu-latest")
        (self.test_dir / "README.md").write_text("# Project\n\nDescription of the project.")

    def test_analyze_infrastructure(self):
        result = analyze_infrastructure(self.test_dir)
        self.assertIn("findings", result)
        self.assertIn("docker", result["findings"])
        self.assertEqual(result["findings"]["docker"]["status"], "FOUND")

    def test_analyze_data_persistence(self):
        result = analyze_data_persistence(self.test_dir)
        self.assertIn("findings", result)
        self.assertEqual(result["findings"]["mongodb"]["status"], "FOUND")

    def test_analyze_backend_api(self):
        result = analyze_backend_api(self.test_dir)
        self.assertIn("findings", result)
        self.assertIn("languages", result["findings"])
        self.assertIn("routes_controllers", result["findings"])

    def test_analyze_frontend(self):
        result = analyze_frontend(self.test_dir)
        self.assertIn("findings", result)
        self.assertIn("frameworks", result["findings"])

    def test_analyze_business_logic(self):
        result = analyze_business_logic(self.test_dir)
        self.assertIn("findings", result)

    def test_analyze_security(self):
        result = analyze_security(self.test_dir)
        self.assertIn("findings", result)

    def test_analyze_devops(self):
        result = analyze_devops(self.test_dir)
        self.assertIn("findings", result)
        self.assertEqual(result["findings"]["ci_cd"]["status"], "FOUND")

    def test_analyze_governance(self):
        result = analyze_governance(self.test_dir)
        self.assertIn("findings", result)
        self.assertEqual(result["findings"]["documentation"]["status"], "FOUND")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)


if __name__ == "__main__":
    unittest.main()
