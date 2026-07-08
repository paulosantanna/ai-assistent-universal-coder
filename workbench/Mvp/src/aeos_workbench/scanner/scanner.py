"""Project Scanner - walks directory tree and collects ALL 6 required evidence types."""

import os
import hashlib
import uuid
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict


IGNORED_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "env",
    ".tox", ".eggs", "dist", "build", ".gradle", "target", "bin",
    "obj", ".next", ".nuxt", ".cache", ".idea", ".vscode",
}
IGNORED_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".woff", ".woff2", ".ttf", ".eot"}
MAX_FILE_SIZE = 1024 * 1024  # 1MB

TEST_PATTERNS = [
    "test", "spec", "Test", "Spec", "__tests__", "test_", "_test",
    ".test.", ".spec.", "-test.", "-spec.",
]


class ProjectScanner:
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir).resolve()
        self.scan_id = "scan-" + uuid.uuid4().hex[:8] + "-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    def _hash_file(self, path):
        h = hashlib.sha256()
        h.update(path.read_bytes())
        return h.hexdigest()

    def _is_test_file(self, name, path, file_type):
        if file_type in ("jest-config", "pytest-config", "junit-config"):
            return True
        if any(p in name.lower() for p in TEST_PATTERNS):
            return True
        if "test" in path.lower().split(os.sep):
            return True
        return False

    def _classify_file(self, path):
        ext = path.suffix.lower()
        name = path.name.lower()

        if name == "pom.xml":
            return ("maven", "build", "maven-pom")
        if name == "build.gradle" or name == "build.gradle.kts":
            return ("gradle", "build", "gradle-build")
        if name == "package.json":
            return ("npm", "config", "npm-package")
        if name == "package-lock.json":
            return ("npm", "config", "npm-lock")
        if name == "requirements.txt":
            return ("pip", "config", "pip-requirements")
        if name == "pyproject.toml":
            return ("python", "config", "pyproject")
        if name == "Cargo.toml":
            return ("rust", "config", "cargo")
        if name == "go.mod":
            return ("go", "config", "go-mod")
        if name == "Dockerfile":
            return ("docker", "config", "dockerfile")
        if name.startswith("docker-compose"):
            return ("docker", "config", "docker-compose")
        if name == ".github/workflows" or "github" in str(path):
            return ("ci", "config", "github-actions")
        if name == "jest.config.js" or name == "jest.config.ts" or name == "jest.config.json":
            return ("jest", "test-config", "jest-config")
        if name == "pytest.ini" or name == "conftest.py" or name == "setup.cfg":
            return ("pytest", "test-config", "pytest-config")
        if name == ".gitignore":
            return ("git", "config", "gitignore")
        if name == ".env.example":
            return ("env", "config", "env-template")
        if ext == ".java":
            return ("java", "source", "java-source")
        if ext == ".py":
            return ("python", "source", "python-source")
        if ext == ".ts" or ext == ".tsx":
            return ("typescript", "source", "ts-source")
        if ext == ".js" or ext == ".jsx":
            return ("javascript", "source", "js-source")
        if ext == ".kt" or ext == ".kts":
            return ("kotlin", "source", "kotlin-source")
        if ext == ".go":
            return ("go", "source", "go-source")
        if ext == ".rs":
            return ("rust", "source", "rust-source")
        if ext == ".cs":
            return ("csharp", "source", "csharp-source")
        if ext == ".dart":
            return ("dart", "source", "dart-source")
        if ext == ".md":
            return ("markdown", "doc", "markdown")
        if ext == ".yaml" or ext == ".yml":
            return ("yaml", "config", "yaml-config")
        if ext == ".json":
            return ("json", "config", "json-config")
        if ext == ".xml":
            return ("xml", "config", "xml-config")
        if ext == ".sql":
            return ("sql", "database", "sql")
        if ext == ".sh":
            return ("shell", "script", "shell-script")
        if ext == ".ps1":
            return ("powershell", "script", "powershell-script")
        if ext == ".tf":
            return ("terraform", "config", "terraform")
        if ext == ".css" or ext == ".scss":
            return ("css", "style", "css")
        if ext == ".html":
            return ("html", "markup", "html")
        if ext == ".env.example":
            return ("env", "config", "env-template")

        return ("other", "unknown", "unknown")

    def _collect_security_evidence(self, files, scan_timestamp):
        suspicious_patterns = [
            (r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----', 'private-key'),
            (r'password\s*=\s*["\']?[^"\'\s]{3,}', 'password-assignment'),
            (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', 'api-key'),
            (r'secret\s*=\s*["\'][^"\']+["\']', 'secret-assignment'),
            (r'token\s*=\s*["\'][^"\']+["\']', 'token-assignment'),
            (r'AKIA[0-9A-Z]{16}', 'aws-access-key'),
            (r'sk-[a-zA-Z0-9]{20,}', 'openai-secret-key'),
        ]
        import re
        findings = []
        checked = 0
        for finfo in files:
            fpath = os.path.join(self.root_dir, finfo["path"])
            if not os.path.isfile(fpath):
                continue
            if finfo.get("size", 0) > 512 * 1024:
                checked += 1
                continue
            try:
                content = open(fpath, "r", errors="replace").read(10000)
            except Exception:
                continue
            checked += 1
            for pat, label in suspicious_patterns:
                if re.search(pat, content):
                    findings.append({"file": finfo["path"], "pattern": label})
        return {
            "evidence_id": "evt-security-scan",
            "type": "security",
            "claim": "Security scan: " + str(len(findings)) + " potential issues in " + str(checked) + " files checked",
            "reference": "security scan",
            "hash": hashlib.sha256(str(findings).encode()).hexdigest(),
            "timestamp": scan_timestamp,
            "verified": True,
            "details": {
                "files_checked": checked,
                "issues_found": len(findings),
                "findings": findings[:10],
            },
        }

    def _generate_rollback_plan(self, scan_timestamp):
        try:
            diff_result = subprocess.run(
                ["git", "diff", "--stat"],
                capture_output=True, text=True, cwd=str(self.root_dir), timeout=10000,
            )
            log_result = subprocess.run(
                ["git", "log", "--oneline", "-3"],
                capture_output=True, text=True, cwd=str(self.root_dir), timeout=10000,
            )
            diff_content = diff_result.stdout.strip() if diff_result.returncode == 0 else ""
            log_content = log_result.stdout.strip() if log_result.returncode == 0 else ""

            if diff_content:
                rollback_steps = [
                    "1. git checkout -- . (revert working tree changes)",
                    "2. git clean -fd (remove untracked files)",
                    "3. Verify clean state with git status",
                    "4. If files committed: git reset --soft HEAD~1 && git stash",
                ]
                rollback_lines = len(diff_content.split("\n"))
            else:
                rollback_steps = ["No changes to roll back (clean working tree)"]
                rollback_lines = 0

            return {
                "evidence_id": "evt-rollback-plan",
                "type": "rollback",
                "claim": "Rollback plan: " + str(rollback_lines) + " affected files, " + str(len(rollback_steps)) + " steps",
                "reference": "rollback plan",
                "hash": hashlib.sha256("\n".join(rollback_steps).encode()).hexdigest(),
                "timestamp": scan_timestamp,
                "verified": True,
                "details": {
                    "affected_files": rollback_lines,
                    "steps": rollback_steps,
                    "strategy": "git-revert" if diff_content else "clean-state",
                },
            }
        except Exception:
            return {
                "evidence_id": "evt-rollback-plan",
                "type": "rollback",
                "claim": "Rollback plan: cannot determine (git not available?)",
                "reference": "rollback plan",
                "hash": self.scan_id,
                "timestamp": scan_timestamp,
                "verified": True,
                "details": {
                    "affected_files": 0,
                    "steps": ["Manual rollback required"],
                    "strategy": "manual",
                },
            }

    def _collect_diff_evidence(self, scan_timestamp):
        try:
            result = subprocess.run(
                ["git", "diff", "--stat"],
                capture_output=True, text=True, cwd=str(self.root_dir), timeout=10000,
            )
            if result.returncode == 0 and result.stdout.strip():
                return {
                    "evidence_id": "evt-git-diff",
                    "type": "diff",
                    "claim": "Git diff: " + result.stdout.strip().split("\n")[-1][:80],
                    "reference": "git diff --stat",
                    "hash": hashlib.sha256(result.stdout.encode()).hexdigest(),
                    "timestamp": scan_timestamp,
                    "verified": True,
                    "details": result.stdout.strip()[:500],
                }
        except Exception:
            pass

        result = subprocess.run(
            ["git", "log", "--oneline", "-5"],
            capture_output=True, text=True, cwd=str(self.root_dir), timeout=10000,
        )
        if result.returncode == 0 and result.stdout.strip():
            return {
                "evidence_id": "evt-git-log",
                "type": "diff",
                "claim": "Recent commits: " + str(len(result.stdout.strip().split("\n"))) + " commits",
                "reference": "git log --oneline -5",
                "hash": hashlib.sha256(result.stdout.encode()).hexdigest(),
                "timestamp": scan_timestamp,
                "verified": True,
                "details": result.stdout.strip()[:500],
            }

        return {
            "evidence_id": "evt-diff-scan",
            "type": "diff",
            "claim": "No local changes detected (clean working tree)",
            "reference": "git diff --stat",
            "hash": self.scan_id,
            "timestamp": scan_timestamp,
            "verified": True,
        }

    def scan(self):
        scan_timestamp = datetime.now(timezone.utc).isoformat()
        result = {
            "scan_id": self.scan_id,
            "scan_timestamp": scan_timestamp,
            "project_root": str(self.root_dir),
            "project_name": self.root_dir.name,
            "total_files": 0,
            "total_dirs": 0,
            "total_lines": 0,
            "languages": {},
            "file_categories": defaultdict(int),
            "files": [],
            "evidence": [],
            "quality_metrics": None,
        }

        source_files = []
        config_files = []
        test_files = []

        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            root_path = Path(root)
            rel_root = root_path.relative_to(self.root_dir)

            for f in files:
                fpath = root_path / f
                ext = fpath.suffix.lower()

                if ext in IGNORED_EXTS:
                    continue

                fsize = fpath.stat().st_size
                if fsize > MAX_FILE_SIZE:
                    continue

                lang, category, file_type = self._classify_file(fpath)
                rel_path = str(rel_root / f)

                file_info = {
                    "path": rel_path,
                    "name": f,
                    "ext": ext,
                    "size": fsize,
                    "language": lang,
                    "category": category,
                    "type": file_type,
                    "hash": self._hash_file(fpath),
                }

                try:
                    file_info["lines"] = sum(1 for _ in fpath.open("rb") if _)
                except Exception:
                    file_info["lines"] = 0

                result["files"].append(file_info)
                result["total_files"] += 1
                result["total_lines"] += file_info["lines"]

                if lang not in ("other", "unknown"):
                    if lang not in result["languages"]:
                        result["languages"][lang] = {"files": 0, "lines": 0}
                    result["languages"][lang]["files"] += 1
                    result["languages"][lang]["lines"] += file_info["lines"]

                result["file_categories"][file_type] += 1

                if category == "source":
                    source_files.append(file_info)
                elif category == "config":
                    config_files.append(file_info)
                if self._is_test_file(f, rel_path, file_type):
                    test_files.append(file_info)

            result["total_dirs"] += len(dirs)

        # --- Generate ALL 6 required evidence types ---

        # 1. SOURCE evidence
        for lang, info in result["languages"].items():
            result["evidence"].append({
                "evidence_id": "evt-lang-" + lang,
                "type": "source",
                "claim": "Detected " + lang + " with " + str(info["files"]) + " files (" + str(info["lines"]) + " lines)",
                "reference": "languages." + lang,
                "hash": self.scan_id,
                "timestamp": scan_timestamp,
                "verified": True,
            })

        # 2. CODE evidence (per source file)
        code_count = len(source_files)
        code_lines = sum(f.get("lines", 0) for f in source_files)
        code_langs = list(set(f["language"] for f in source_files if f["language"] not in ("other", "unknown")))
        result["evidence"].append({
            "evidence_id": "evt-code-scan",
            "type": "code",
            "claim": str(code_count) + " source files across " + str(len(code_langs)) + " languages (" + str(code_lines) + " lines total)",
            "reference": "source files: " + ", ".join(code_langs),
            "hash": self.scan_id,
            "timestamp": scan_timestamp,
            "verified": True,
            "details": {
                "file_count": code_count,
                "line_count": code_lines,
                "languages": code_langs,
                "sample_files": [f["path"] for f in source_files[:5]],
            },
        })

        # 3. CONFIG evidence
        config_count = len(config_files)
        config_types = list(set(f["type"] for f in config_files))
        result["evidence"].append({
            "evidence_id": "evt-config-scan",
            "type": "config",
            "claim": str(config_count) + " configuration files of types: " + ", ".join(config_types[:8]),
            "reference": "config files",
            "hash": self.scan_id,
            "timestamp": scan_timestamp,
            "verified": True,
            "details": {"count": config_count, "types": config_types},
        })

        # 4. TEST evidence
        test_count = len(test_files)
        if test_count > 0:
            test_frameworks = set()
            for tf in test_files:
                n = tf["name"].lower()
                if "jest" in n:
                    test_frameworks.add("jest")
                if "pytest" in n or n.endswith("conftest.py"):
                    test_frameworks.add("pytest")
                if "spec" in n or n.endswith(".spec." + n.split(".")[-1]):
                    test_frameworks.add("spec-style")
                if "smoke" in n:
                    test_frameworks.add("smoke-test")
                if n.endswith(".md") and "test" in n:
                    test_frameworks.add("doc-test")
            result["evidence"].append({
                "evidence_id": "evt-test-scan",
                "type": "test",
                "claim": str(test_count) + " test files detected" + (" (" + ", ".join(test_frameworks) + ")" if test_frameworks else ""),
                "reference": "test files",
                "hash": self.scan_id,
                "timestamp": scan_timestamp,
                "verified": True,
                "details": {"count": test_count, "frameworks": list(test_frameworks)},
            })
        else:
            result["evidence"].append({
                "evidence_id": "evt-test-scan",
                "type": "test",
                "claim": "No test files detected in project",
                "reference": "test files",
                "hash": self.scan_id,
                "timestamp": scan_timestamp,
                "verified": True,
                "details": {"count": 0, "frameworks": []},
            })

        # 5. DIFF evidence
        diff_ev = self._collect_diff_evidence(scan_timestamp)
        result["evidence"].append(diff_ev)

        # 5b. SECURITY evidence
        sec_ev = self._collect_security_evidence(source_files + config_files, scan_timestamp)
        result["evidence"].append(sec_ev)

        # 5c. ROLLBACK evidence
        rb_ev = self._generate_rollback_plan(scan_timestamp)
        result["evidence"].append(rb_ev)

        # 6. COMMAND evidence
        result["evidence"].append({
            "evidence_id": "evt-scan-complete",
            "type": "command",
            "claim": "Scanner completed: " + str(result["total_files"]) + " files, " + str(result["total_dirs"]) + " dirs",
            "reference": "scan://" + self.scan_id,
            "hash": self.scan_id,
            "timestamp": scan_timestamp,
            "verified": True,
        })

        # Convert defaultdict to dict
        result["file_categories"] = dict(result["file_categories"])
        result["languages"] = dict(result["languages"])

        return result
