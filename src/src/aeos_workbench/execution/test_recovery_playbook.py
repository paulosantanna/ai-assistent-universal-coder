"""Test Recovery Playbook — analyze test coverage and generate test stubs in sandbox."""

from datetime import datetime, timezone
from pathlib import Path

from aeos_workbench.scanner.scanner import ProjectScanner
from aeos_workbench.stack_detector.detector import StackDetector

TEST_FRAMEWORKS = {
    "pytest": {
        "patterns": ["pytest", "conftest.py", "pytest.ini", "test_"],
        "file_types": ["pytest-config", "python-source"],
        "language": "python",
    },
    "jest": {
        "patterns": ["jest", ".test.js", ".spec."],
        "file_types": ["jest-config", "ts-source", "js-source"],
        "language": "typescript",
    },
    "junit": {
        "patterns": ["junit", "@Test", "@org.junit"],
        "file_types": ["java-source"],
        "language": "java",
    },
    "mocha": {
        "patterns": ["mocha", "describe(", "it("],
        "file_types": ["ts-source", "js-source"],
        "language": "javascript",
    },
    "xunit": {
        "patterns": ["xunit", "Xunit", "[Fact]", "[Theory]"],
        "file_types": ["csharp-source"],
        "language": "csharp",
    },
    "gotest": {
        "patterns": ["_test.go", "Test", "testing.T"],
        "file_types": ["go-source"],
        "language": "go",
    },
}


class TestRecoveryPlaybook:
    def __init__(self, sandbox_writer, rollback_manager, step_engine, execution_id: str, reports_dir: Path):
        self.sandbox_writer = sandbox_writer
        self.rollback_manager = rollback_manager
        self.step_engine = step_engine
        self.execution_id = execution_id
        self.reports_dir = reports_dir / execution_id
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.generated_artifacts: list[dict] = []
        self.risks: list[str] = []
        self.source_stubs_dir = "generated-tests"

    def execute(self, target_path: Path) -> dict:
        step_id = self.step_engine.register_step({
            "step_id": "test-recovery-analysis",
            "skill": "test-generation",
            "status": "running",
            "inputs": {"target_path": str(target_path)},
            "outputs": {},
            "evidence": [],
            "permission_decisions": [],
            "risks": [],
            "errors": [],
        })

        scanner = ProjectScanner(target_path)
        scan_result = scanner.scan()
        detector = StackDetector(scan_result)
        stacks = detector.detect()

        test_frameworks, test_files, source_no_tests = self._detect_tests(scan_result)

        self.step_engine.update_step(step_id, {
            "status": "completed",
            "outputs": {
                "total_files": scan_result.get("total_files", 0),
                "test_frameworks": list(test_frameworks.keys()),
                "test_file_count": len(test_files),
                "source_files_without_tests": len(source_no_tests),
            },
            "evidence": [
                {"type": "test-analysis", "frameworks": len(test_frameworks), "test_files": len(test_files)}
            ],
        })
        self.step_engine.save_all()

        self._generate_report(scan_result, test_frameworks, test_files, source_no_tests, stacks)

        for source_file in source_no_tests[:5]:
            self._generate_test_stub(source_file, test_frameworks, scan_result)

        return {
            "generated_artifacts": self.generated_artifacts,
            "risks": self.risks,
            "test_frameworks_detected": list(test_frameworks.keys()),
            "source_files_without_tests": len(source_no_tests),
        }

    def _detect_tests(self, scan_result):
        test_frameworks = {}
        test_files = []
        source_no_tests = []
        files = scan_result.get("files", [])

        for fw_id, fw_def in TEST_FRAMEWORKS.items():
            test_frameworks[fw_id] = {"count": 0, "files": [], "confidence": 0}

        for f in files:
            fname = f.get("name", "")
            fpath = f.get("path", "")
            ftype = f.get("type", "")
            lang = f.get("language", "")

            is_test = False
            for fw_id, fw_def in TEST_FRAMEWORKS.items():
                if fw_def["language"] != lang and lang != "all":
                    continue
                for pat in fw_def["patterns"]:
                    if pat.lower() in fname.lower() or pat in fpath.lower():
                        is_test = True
                        test_frameworks[fw_id]["count"] += 1
                        test_frameworks[fw_id]["files"].append(fpath)
                        if fpath not in test_files:
                            test_files.append(fpath)
                        break
                if is_test:
                    break

            if not is_test and lang not in ("other", "unknown"):
                for part in fpath.lower().replace("\\", "/").split("/"):
                    if part in ("test", "tests", "__spec__"):
                        is_test = True
                        break
                if not is_test:
                    source_no_tests.append(f)

        for fw_id in test_frameworks:
            if test_frameworks[fw_id]["count"] > 0:
                total = len([f for f in files if f.get("language") == TEST_FRAMEWORKS[fw_id]["language"]])
                ratio = test_frameworks[fw_id]["count"] / max(total, 1)
                test_frameworks[fw_id]["confidence"] = round(min(ratio * 2, 1.0), 2)

        return test_frameworks, test_files, source_no_tests

    def _generate_report(self, scan_result, test_frameworks, test_files, source_no_tests, stacks):
        fw_list = [(k, v) for k, v in test_frameworks.items() if v["count"] > 0]
        total_source = len(scan_result.get("files", []))
        coverage_pct = round(len(test_files) / max(total_source, 1) * 100, 1) if test_files else 0.0

        content = [
            "# Test Recovery Report",
            "",
            "**Execution ID:** " + self.execution_id,
            "**Generated At:** " + datetime.now(timezone.utc).isoformat(),
            "",
            "## Summary",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            "| Total Files | " + str(scan_result.get("total_files", 0)) + " |",
            "| Test Files Found | " + str(len(test_files)) + " |",
            "| Source Files Without Tests | " + str(len(source_no_tests)) + " |",
            "| Estimated Coverage | " + str(coverage_pct) + "% |",
            "",
            "## Detected Test Frameworks",
            "",
            "| Framework | Test Files | Confidence |",
            "|-----------|-----------|------------|",
        ]
        for fw_id, fw_data in fw_list:
            content.append("| " + fw_id + " | " + str(fw_data["count"]) + " | " + str(fw_data["confidence"]) + " |")
        if not fw_list:
            content.append("| *(no test frameworks detected)* | 0 | 0.0 |")

        content.append("")
        content.append("## Source Files Without Tests (Top 20)")
        content.append("")
        content.append("| # | File | Language | Suggested Test Framework |")
        content.append("|---|------|----------|-------------------------|")
        for i, f in enumerate(source_no_tests[:20], 1):
            suggested = self._suggest_framework(f, test_frameworks)
            content.append("| " + str(i) + " | `" + f.get("path", "?") + "` | " + f.get("language", "?") + " | " + suggested + " |")
        if not source_no_tests:
            content.append("| *(all source files have tests)* | | | |")

        content.append("")
        content.append("## Recovery Plan")
        content.append("")
        content.append("1. **Priority 1:** Add tests for files detected as critical (no test coverage)")
        content.append("2. **Priority 2:** Add integration tests for core modules")
        content.append("3. **Priority 3:** Add edge case tests for utility functions")
        content.append("")
        content.append("### Generated Test Stubs")
        content.append("")
        content.append("The following test stubs were generated in sandbox:")
        for f in source_no_tests[:5]:
            stub_name = self._stub_name(f)
            content.append("- `.aeos/sandbox/" + self.execution_id + "/generated-tests/" + stub_name + "`")

        content.append("")
        content.append("## Notes")
        content.append("- Generated test stubs are in `.aeos/sandbox/" + self.execution_id + "/generated-tests/`")
        content.append("- No real test files were modified")
        content.append("- Review generated stubs before moving to src/test/")

        report_content = "\n".join(content)
        report_path = self.reports_dir / "test-recovery-report.md"
        report_path.write_text(report_content, encoding="utf-8")
        self.rollback_manager.register_generated_file(report_path, "reports/" + self.execution_id + "/test-recovery-report.md", report_content[:100])

        self.generated_artifacts.append({
            "name": "test-recovery-report.md",
            "path": str(report_path),
            "type": "test-report",
            "size": len(report_content.encode("utf-8")),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def _suggest_framework(self, f, test_frameworks):
        lang = f.get("language", "")
        for fw_id, fw_data in test_frameworks.items():
            if fw_data["count"] > 0 and TEST_FRAMEWORKS.get(fw_id, {}).get("language") == lang:
                return fw_id
        lang_map = {"python": "pytest", "typescript": "jest", "java": "junit", "go": "gotest", "csharp": "xunit", "rust": "cargo-test"}
        return lang_map.get(lang, "unknown")

    def _stub_name(self, f):
        path = f.get("path", "")
        name = f.get("name", "")
        ext = f.get("ext", "")
        base = name.rsplit(".", 1)[0] if "." in name else name
        test_ext_map = {".py": "_test.py", ".ts": ".test.ts", ".tsx": ".test.tsx", ".js": ".test.js", ".jsx": ".test.jsx", ".java": "Test.java", ".go": "_test.go", ".cs": "Test.cs"}
        test_ext = test_ext_map.get(ext, ".test" + ext)
        parts = path.split("/")
        parts[-1] = base.replace(".", "_") + test_ext
        return "/".join(parts)

    def _generate_test_stub(self, source_file, test_frameworks, scan_result):
        ext = source_file.get("ext", "")
        name = source_file.get("name", "")

        generators = {
            ".py": self._generate_python_test_stub,
            ".ts": self._generate_typescript_test_stub,
            ".tsx": self._generate_typescript_test_stub,
            ".js": self._generate_javascript_test_stub,
            ".jsx": self._generate_javascript_test_stub,
            ".java": self._generate_java_test_stub,
            ".go": self._generate_go_test_stub,
        }

        gen = generators.get(ext)
        if not gen:
            return

        stub_content = gen(name, source_file.get("path", ""))
        stub_rel = str(self.source_stubs_dir / self._stub_name(source_file))
        sandbox_path = self.stub_writer_write(stub_rel, stub_content)
        self.rollback_manager.register_generated_file(sandbox_path, str(stub_rel), stub_content[:100])
        self.generated_artifacts.append({
            "name": str(stub_rel),
            "path": str(sandbox_path),
            "type": "test-stub",
            "size": len(stub_content.encode("utf-8")),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def stub_writer_write(self, rel_path, content):
        return self.sandbox_writer.write(rel_path, content)

    def _generate_python_test_stub(self, name, path):
        lines = [
            '"""Test stub for ' + name + '"""',
            "import pytest",
            "",
            "",
            "class Test" + name.replace(".py", "").title().replace("_", "") + ":",
            '    """Tests for ' + path + '."""',
            "",
            "    def test_placeholder(self):",
            '        """TODO: Implement test."""',
            "        assert True",
        ]
        return "\n".join(lines)

    def _generate_typescript_test_stub(self, name, path):
        base = name.replace(".ts", "").replace(".tsx", "")
        lines = [
            "// Test stub for " + path,
            "",
            "describe('" + base + "', () => {",
            "  it('should work', () => {",
            "    // TODO: Implement test",
            "    expect(true).toBe(true);",
            "  });",
            "});",
        ]
        return "\n".join(lines)

    def _generate_javascript_test_stub(self, name, path):
        base = name.replace(".js", "").replace(".jsx", "")
        lines = [
            "// Test stub for " + path,
            "",
            "describe('" + base + "', () => {",
            "  it('should work', () => {",
            "    // TODO: Implement test",
            "    expect(true).toBe(true);",
            "  });",
            "});",
        ]
        return "\n".join(lines)

    def _generate_java_test_stub(self, name, path):
        class_name = name.replace(".java", "")
        lines = [
            "import org.junit.jupiter.api.Test;",
            "import static org.junit.jupiter.api.Assertions.*;",
            "",
            "/**",
            " * Auto-generated test stub for " + path,
            " */",
            "public class " + class_name + "Test {",
            "",
            "    @Test",
            "    void testPlaceholder() {",
            "        // TODO: Implement test",
            "        assertTrue(true);",
            "    }",
            "}",
        ]
        return "\n".join(lines)

    def _generate_go_test_stub(self, name, path):
        pkg = name.replace("_test.go", "").replace(".go", "")
        lines = [
            "package " + pkg,
            "",
            'import "testing"',
            "",
            "// Test stub for " + path,
            "func TestPlaceholder(t *testing.T) {",
            "    // TODO: Implement test",
            "}",
        ]
        return "\n".join(lines)