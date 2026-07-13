from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[2] / "scripts" / "toolchain_doctor.py"
sys.path.insert(0, str(MODULE_PATH.parent))
spec = importlib.util.spec_from_file_location("toolchain_doctor", MODULE_PATH)
toolchain_doctor = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules["toolchain_doctor"] = toolchain_doctor
spec.loader.exec_module(toolchain_doctor)


def test_toolchain_doctor_marks_missing_optional_java_as_adapter_covered(tmp_path: Path):
    statuses = toolchain_doctor.evaluate(tmp_path)

    java_maven = next(item for item in statuses if item.name == "java-maven")

    assert java_maven.status == "adapter"
    assert java_maven.optional is True
    assert java_maven.fallback == "ecosystem-contract-adapter"
    assert "Maven distribution is not present" in java_maven.reason


def test_toolchain_doctor_json_summary_counts_adapter_coverage(tmp_path: Path):
    payload = json.loads(toolchain_doctor.render_json(toolchain_doctor.evaluate(tmp_path)))

    assert payload["summary"]["adapter_covered"] >= 5
    assert payload["summary"]["optional_skipped"] == 0
    assert any(item["name"] == "dotnet" and item["status"] == "adapter" for item in payload["toolchains"])


def test_toolchain_doctor_can_require_optional_toolchains(tmp_path: Path):
    exit_code = toolchain_doctor.main(["--root", str(tmp_path), "--require-optional"])

    assert exit_code == 1
