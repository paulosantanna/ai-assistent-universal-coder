import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backends.common import Response, TransportError, UrllibTransport, load_json
from backends.executables import check as check_executables
from backends.pe import build_pe, parse_pe
from backends.sast import check as check_sast
from engine import run
from prepush import install_hook


NOW = datetime(2026, 11, 9, 20, 0, tzinfo=timezone.utc)
FRESH = "Mon, 09 Nov 2026 19:18:28 GMT"
STALE = "Mon, 01 Jan 2024 00:00:00 GMT"
PREPUSH = Path(__file__).resolve().parents[1]
POLICY = load_json(PREPUSH / "policy.json")
SAST = load_json(PREPUSH / "catalogs" / "sast.json")
SECURITY = load_json(PREPUSH / "catalogs" / "security.json")
PYTHON_FEED = [
    {"cycle": "3.15", "releaseDate": "2026-10-09", "eol": "2031-10-31", "latest": "3.15.2"},
    {"cycle": "3.12", "releaseDate": "2023-10-02", "eol": "2028-10-31", "latest": "3.12.12"},
]
NODE_FEED = [
    {"cycle": "26", "releaseDate": "2026-05-05", "eol": "2029-04-30", "latest": "26.13.0"},
    {"cycle": "20", "releaseDate": "2023-04-18", "eol": "2026-04-30", "latest": "20.19.0"},
]


class FakeTransport:
    def __init__(self, routes):
        self.routes = routes

    def request(self, method, url, body=None, headers=None, timeout=30):
        if url not in self.routes:
            raise TransportError(f"sem rota {method} {url}")
        status, hdrs, payload = self.routes[url]
        if not isinstance(payload, bytes):
            payload = json.dumps(payload).encode("utf-8")
        return Response(status, {key.lower(): value for key, value in hdrs.items()}, payload)


class Offline:
    def request(self, method, url, body=None, headers=None, timeout=30):
        raise TransportError("offline")


def routes(query=None, pypi="1.2.3", modified=FRESH, sast_sha=None, gitleaks="v8.30.1", python_feed=None, node=False):
    query = {"results": [{}]} if query is None else query
    table = {
        POLICY["osv_exports"]["PyPI"]: (200, {"Last-Modified": modified}, b""),
        POLICY["osv_query"]: (200, {}, query),
        POLICY["registries"]["PyPI"].format(name="demo"): (200, {}, {"info": {"version": pypi}}),
        POLICY["endoflife"].format(product="python"): (200, {}, python_feed or PYTHON_FEED),
        SAST["upstream"]: (200, {}, {"sha": sast_sha or SAST["aligned_upstream"]}),
        SECURITY["upstream"]: (200, {}, {"tag_name": gitleaks}),
    }
    if node:
        table[POLICY["endoflife"].format(product="node")] = (200, {}, NODE_FEED)
    return table


def write(root: Path, rel: str, text: str):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


class PrepushTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def green_files(self):
        write(self.root, "requirements.txt", "demo==1.2.3\n")
        write(self.root, "app.py", "print('ok')\n")
        write(
            self.root,
            ".github/workflows/ci.yml",
            "name: ci\njobs:\n  test:\n    steps:\n"
            "      - uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97\n"
            "        with:\n          python-version: '3.15'\n",
        )

    def execute(self, table, runtime=None, exceptions=None):
        path = self.root / "exceptions.json"
        path.write_text(json.dumps({"exceptions": exceptions or []}), encoding="utf-8")
        return run(
            self.root,
            POLICY,
            FakeTransport(table),
            NOW,
            runtime or {"python": "3.15.2", "node": None},
            PREPUSH / "catalogs",
            path,
        )

    def codes(self, report, backend):
        found = next(item for item in report["backends"] if item["id"] == backend)
        return found["status"], {item["code"] for item in found["findings"]}

    def test_pe_roundtrip_reads_creator_and_version(self):
        stamp = int(NOW.timestamp()) - 3600
        data = build_pe(stamp, {"CompanyName": "CodENavi", "FileVersion": "1.2.3", "ProductName": "App"})
        parsed = parse_pe(data)
        self.assertEqual(parsed["timestamp"], stamp)
        self.assertEqual(parsed["strings"]["CompanyName"], "CodENavi")
        self.assertEqual(parsed["strings"]["FileVersion"], "1.2.3")

    def test_clean_repository_passes(self):
        self.green_files()
        report = self.execute(routes())
        self.assertEqual(report["status"], "pass", json.dumps(report, ensure_ascii=False))

    def test_cve_blocks_and_ignores_withdrawn(self):
        self.green_files()
        vuln = {"id": "GHSA-1", "aliases": ["CVE-2026-1000"], "summary": "real"}
        withdrawn = {"id": "GHSA-2", "withdrawn": "2026-01-01T00:00:00Z"}
        report = self.execute(routes(query={"results": [{"vulns": [vuln, withdrawn]}]}))
        status, codes = self.codes(report, "cve_google")
        self.assertEqual(status, "fail")
        self.assertEqual(codes, {"cve-found"})
        self.assertIn("CVE-2026-1000", report["backends"][0]["findings"][0]["message"])

    def test_stale_osv_export_blocks(self):
        self.green_files()
        report = self.execute(routes(modified=STALE))
        status, codes = self.codes(report, "cve_google")
        self.assertEqual(status, "blocked")
        self.assertIn("cve-export-stale", codes)
        self.assertEqual(report["status"], "blocked")

    def test_outdated_and_unpinned_libraries_fail(self):
        write(self.root, "requirements.txt", "demo==1.0.0\n")
        write(self.root, "package.json", json.dumps({"dependencies": {"leftpad": "^1.0.0"}}))
        report = self.execute(routes(pypi="1.2.3"))
        status, codes = self.codes(report, "libraries")
        self.assertEqual(status, "fail")
        self.assertIn("library-outdated", codes)
        self.assertIn("library-unpinned", codes)

    def test_old_language_cycle_and_range_fail(self):
        write(self.root, ".github/workflows/ci.yml", "python-version: '3.12'\nnode-version: '20'\n")
        write(self.root, "pyproject.toml", "[project]\nrequires-python = '>=3.12,<3.13'\n")
        report = self.execute(routes(node=True), {"python": "3.12.12", "node": "20.19.0"})
        status, codes = self.codes(report, "language")
        self.assertEqual(status, "fail")
        self.assertIn("language-outdated", codes)
        self.assertGreaterEqual(len(next(item for item in report["backends"] if item["id"] == "language")["findings"]), 3)

    def test_current_language_range_passes(self):
        self.green_files()
        write(self.root, "pyproject.toml", "[project]\nrequires-python = '>=3.15'\n")
        report = self.execute(routes())
        self.assertEqual(self.codes(report, "language"), ("pass", set()))

    def test_executable_creator_version_and_age(self):
        fresh = build_pe(int(NOW.timestamp()) - 3600, {"CompanyName": "CodENavi", "FileVersion": "1.2.3"})
        stale = build_pe(int((NOW - timedelta(days=120)).timestamp()), {"CompanyName": "CodENavi", "FileVersion": "1.2.3"})
        anonymous = build_pe(int(NOW.timestamp()) - 3600, {"FileVersion": "1.2.3"})
        write(self.root, "bin/app.exe", "")
        (self.root / "bin/app.exe").write_bytes(fresh)
        report = self.execute(routes())
        self.assertEqual(self.codes(report, "executables"), ("pass", set()))
        (self.root / "bin/app.exe").write_bytes(stale)
        report = self.execute(routes())
        self.assertIn("exe-stale", self.codes(report, "executables")[1])
        (self.root / "bin/app.exe").write_bytes(anonymous)
        report = self.execute(routes())
        self.assertIn("exe-creator-missing", self.codes(report, "executables")[1])
        parsed = check_executables(self.root, POLICY, None, NOW)
        self.assertEqual(parsed.evidence["executables"][0]["file_version"], "1.2.3")

    def test_sast_finds_eval_not_method_call_and_rejects_old_catalog(self):
        write(self.root, "app.py", "value = eval('1')\nmodel.eval()\n")
        report = self.execute(routes())
        status, codes = self.codes(report, "sast")
        self.assertEqual(status, "fail")
        self.assertEqual(codes, {"py-eval"})
        self.assertEqual(len(next(item for item in report["backends"] if item["id"] == "sast")["findings"]), 1)
        catalog = self.root / "sast.json"
        old = dict(SAST)
        old["aligned_upstream"] = "0" * 40
        catalog.write_text(json.dumps(old), encoding="utf-8")
        result = check_sast(self.root, POLICY, FakeTransport(routes()), NOW, catalog)
        self.assertIn("sast-catalog-behind-upstream", {item["code"] for item in result.findings})

    def test_security_secret_and_unpinned_action(self):
        write(self.root, "token.txt", "ghp_" + ("a" * 36) + "\n")
        write(self.root, ".github/workflows/ci.yml", "on: pull_request_target\njobs:\n  t:\n    steps:\n      - uses: actions/checkout@v4\n")
        report = self.execute(routes())
        status, codes = self.codes(report, "security")
        self.assertEqual(status, "fail")
        self.assertIn("possible-secret", codes)
        self.assertIn("action-unpinned", codes)
        self.assertIn("workflow-pull-request-target", codes)
        self.assertNotIn("ghp_", json.dumps(report))

    def test_local_action_is_allowed(self):
        self.green_files()
        write(self.root, ".github/workflows/ci.yml", "jobs:\n  t:\n    steps:\n      - uses: ./.github/workflows/local.yml\n")
        write(self.root, ".github/workflows/local.yml", "python-version: '3.15'\n")
        report = self.execute(routes())
        self.assertEqual(self.codes(report, "security")[0], "pass")

    def test_excluded_tree_is_not_scanned(self):
        self.green_files()
        write(self.root, "00_skills/evil.py", "eval('x')\n")
        write(self.root, ".venv/Lib/site-packages/evil.py", "eval('x')\n")
        write(self.root, ".state/runtime/java/bin/java.exe", "")
        (self.root / ".state/runtime/java/bin/java.exe").write_bytes(b"MZ-not-a-real-pe")
        report = self.execute(routes())
        self.assertEqual(report["status"], "pass", json.dumps(report, ensure_ascii=False))

    def test_expired_exception_does_not_waive(self):
        write(self.root, "requirements.txt", "demo>=1\n")
        expired = {"backend": "libraries", "code": "library-unpinned", "subject": "PyPI:demo", "expires": "2026-11-08T00:00:00Z", "reason": "velha"}
        report = self.execute(routes(), exceptions=[expired])
        self.assertIn("library-unpinned", self.codes(report, "libraries")[1])
        active = dict(expired)
        active["expires"] = "2026-12-01T00:00:00Z"
        report = self.execute(routes(), exceptions=[active])
        self.assertEqual(self.codes(report, "libraries"), ("pass", set()))

    def test_offline_refresh_blocks(self):
        self.green_files()
        report = run(self.root, POLICY, Offline(), NOW, {"python": "3.15.2", "node": None}, PREPUSH / "catalogs", PREPUSH / "exceptions.json")
        self.assertEqual(report["status"], "blocked")
        for backend in report["backends"]:
            if backend["id"] == "executables":
                self.assertEqual(backend["status"], "pass")
            else:
                self.assertEqual(backend["status"], "blocked", backend["id"])

    def test_github_token_stays_on_api_github(self):
        captured = []

        class Res:
            status = 200
            headers = {}

            def read(self):
                return b"{}"

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

        def fake_urlopen(req, timeout=30):
            captured.append((req.full_url, req.get_header("Authorization")))
            return Res()

        transport = UrllibTransport()
        with patch.dict(os.environ, {"GITHUB_TOKEN": "ghs_testtoken", "GH_TOKEN": ""}, clear=False):
            with patch("urllib.request.urlopen", fake_urlopen):
                transport.request("GET", "https://api.github.com/repos/gitleaks/gitleaks/releases/latest")
                transport.request("GET", "https://pypi.org/pypi/demo/json")
                transport.request("GET", "https://api.github.com/rate_limit", headers={"Authorization": "Bearer already"})
        self.assertEqual(captured[0][1], "Bearer ghs_testtoken")
        self.assertIsNone(captured[1][1])
        self.assertEqual(captured[2][1], "Bearer already")
        with patch.dict(os.environ, {"GITHUB_TOKEN": "", "GH_TOKEN": "ghs_fallback"}, clear=False):
            with patch("urllib.request.urlopen", fake_urlopen):
                transport.request("GET", "https://api.github.com/rate_limit")
        self.assertEqual(captured[3][1], "Bearer ghs_fallback")

    def test_hook_install_uses_lf(self):
        subprocess.run(["git", "init", str(self.root)], check=True, capture_output=True)
        destination = install_hook(self.root)
        data = destination.read_bytes()
        self.assertNotIn(b"\r", data)
        self.assertIn(b"quality/prepush/prepush.py", data)


if __name__ == "__main__":
    unittest.main()
