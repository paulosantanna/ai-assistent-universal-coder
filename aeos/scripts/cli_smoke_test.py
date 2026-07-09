#!/usr/bin/env python3
"""
AEOS CLI Smoke Test
Tests all major CLI commands via module imports.
"""
import sys
import json
from pathlib import Path
from unittest.mock import MagicMock, patch
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))


def test_version():
    from aeos.cli.commands.version import cmd_version
    args = MagicMock()
    code = cmd_version(args)
    assert code == 0, f"version failed: {code}"
    print("  [PASS] version")


def test_init(tmp_path: Path):
    from aeos.cli.commands.init import cmd_init
    args = MagicMock()
    args.target = str(tmp_path)
    code = cmd_init(args)
    assert code == 0, f"init failed: {code}"
    assert (tmp_path / ".aeos" / "evidence").exists()
    assert (tmp_path / ".aeos" / "reports").exists()
    print("  [PASS] init")


def test_doctor(tmp_path: Path):
    from aeos.cli.commands.doctor import cmd_doctor
    (tmp_path / ".aeos" / "config").mkdir(parents=True, exist_ok=True)
    (tmp_path / ".aeos" / "registries").mkdir(parents=True, exist_ok=True)
    (tmp_path / ".aeos" / "evidence").mkdir(parents=True, exist_ok=True)
    (tmp_path / ".aeos" / "reports").mkdir(parents=True, exist_ok=True)
    (tmp_path / ".aeos" / "config" / "permissions.yaml").write_text("permissions: []")
    (tmp_path / ".aeos" / "config" / "policies.yaml").write_text("policies: []")
    (tmp_path / ".aeos" / "registries" / "skills.yaml").write_text("skills: {}")
    (tmp_path / "pytest.ini").write_text("[pytest]\n")
    args = MagicMock()
    args.target = str(tmp_path)
    code = cmd_doctor(args)
    assert code in (0, 3), f"doctor failed: {code}"
    report = tmp_path / ".aeos" / "reports" / "doctor-report.md"
    assert report.exists()
    print("  [PASS] doctor")


def test_registry_validate(tmp_path: Path):
    from aeos.cli.commands.registry import cmd_registry_validate
    reg_dir = tmp_path / ".aeos" / "registries"
    reg_dir.mkdir(parents=True, exist_ok=True)
    (reg_dir / "skills.yaml").write_text("skills: {}")
    args = MagicMock()
    args.target = str(tmp_path)
    code = cmd_registry_validate(args)
    assert code in (0, 1), f"registry validate failed: {code}"
    print("  [PASS] registry validate")


def test_registry_list(tmp_path: Path):
    from aeos.cli.commands.registry import cmd_registry_list
    reg_dir = tmp_path / ".aeos" / "registries"
    reg_dir.mkdir(parents=True, exist_ok=True)
    (reg_dir / "skills.yaml").write_text("skills: {test-skill: {}}")
    args = MagicMock()
    args.target = str(tmp_path)
    args.entity = "skills"
    code = cmd_registry_list(args)
    assert code == 0, f"registry list failed: {code}"
    print("  [PASS] registry list")


def test_evidence_verify(tmp_path: Path):
    from aeos.cli.commands.evidence import cmd_evidence_verify
    ev_dir = tmp_path / ".aeos" / "evidence" / "exec-smoke"
    ev_dir.mkdir(parents=True, exist_ok=True)
    (ev_dir / "runtime-request.jsonl").write_text('{"test": true}')
    from aeos.core.evidence.evidence_manifest import StagedManifestBuilder
    builder = StagedManifestBuilder(execution_id="exec-smoke", evidence_dir=str(ev_dir), workspace_root=str(tmp_path))
    builder.finalize_runtime_manifest()
    args = MagicMock()
    args.target = str(tmp_path)
    args.execution_id = "exec-smoke"
    code = cmd_evidence_verify(args)
    assert code in (0, 1), f"evidence verify failed: {code}"
    print("  [PASS] evidence verify")


def test_evidence_list(tmp_path: Path):
    from aeos.cli.commands.evidence import cmd_evidence_list
    ev_dir = tmp_path / ".aeos" / "evidence" / "exec-list"
    ev_dir.mkdir(parents=True, exist_ok=True)
    (ev_dir / "runtime-request.jsonl").write_text('{}')
    args = MagicMock()
    args.target = str(tmp_path)
    code = cmd_evidence_list(args)
    assert code == 0, f"evidence list failed: {code}"
    print("  [PASS] evidence list")


def test_evidence_report(tmp_path: Path):
    from aeos.cli.commands.evidence import cmd_evidence_report
    ev_dir = tmp_path / ".aeos" / "evidence" / "exec-rpt"
    ev_dir.mkdir(parents=True, exist_ok=True)
    (ev_dir / "runtime-request.jsonl").write_text('{"test": true}')
    args = MagicMock()
    args.target = str(tmp_path)
    args.execution_id = "exec-rpt"
    code = cmd_evidence_report(args)
    assert code in (0, 2), f"evidence report failed: {code}"
    print("  [PASS] evidence report")


def test_runtime_command_handlers():
    from aeos.cli.commands.run_skill import _status_to_exit
    assert _status_to_exit("PASS") == 0
    assert _status_to_exit("BLOCKED") == 1
    assert _status_to_exit("ERROR") == 2
    assert _status_to_exit("REVIEW") == 3
    from aeos.cli.commands.run_skill import cmd_skill_run
    from aeos.cli.commands.run_playbook import cmd_playbook_run
    from aeos.cli.commands.run_agent import cmd_agent_run
    print("  [PASS] runtime command handlers load correctly")


def main():
    import tempfile
    print("=" * 60)
    print("AEOS CLI Smoke Test")
    print("=" * 60)
    failures = 0
    tests = [
        ("version", test_version),
        ("init", lambda: test_init(Path(tempfile.mkdtemp()))),
        ("doctor", lambda: test_doctor(Path(tempfile.mkdtemp()))),
        ("registry_validate", lambda: test_registry_validate(Path(tempfile.mkdtemp()))),
        ("registry_list", lambda: test_registry_list(Path(tempfile.mkdtemp()))),
        ("evidence_verify", lambda: test_evidence_verify(Path(tempfile.mkdtemp()))),
        ("evidence_list", lambda: test_evidence_list(Path(tempfile.mkdtemp()))),
        ("evidence_report", lambda: test_evidence_report(Path(tempfile.mkdtemp()))),
        ("runtime_handlers", test_runtime_command_handlers),
    ]
    for name, fn in tests:
        try:
            fn()
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")
            import traceback
            traceback.print_exc()
            failures += 1
    print()
    if failures == 0:
        print(f"CLI SMOKE TEST PASSED ({len(tests)}/{len(tests)})")
        return 0
    else:
        print(f"CLI SMOKE TEST FAILED ({len(tests)-failures}/{len(tests)} failures={failures})")
        return 1


if __name__ == "__main__":
    sys.exit(main())