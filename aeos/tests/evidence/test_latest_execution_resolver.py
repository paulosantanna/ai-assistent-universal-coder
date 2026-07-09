import pytest
from pathlib import Path
from aeos.core.evidence.execution_resolver import (
    resolve_execution,
    format_resolved,
    RESOLVE_LATEST_ANY,
    RESOLVE_LATEST_COMPLETE,
    RESOLVE_LATEST_JUDGE,
    RESOLVE_LATEST_RUNTIME,
    normalize_mode,
)


def _make_execution(workspace_root: Path, eid: str, has_evidence: bool = False,
                    has_judge: bool = False, has_runtime: bool = False):
    d = workspace_root / ".aeos" / "evidence" / eid
    d.mkdir(parents=True, exist_ok=True)
    (d / "dummy.txt").write_text("x")
    if has_evidence:
        (d / "evidence-manifest.json").write_text('{}')
    if has_judge:
        (d / "judge-result.json").write_text('{}')
    if has_runtime:
        (d / "runtime-evidence-manifest.json").write_text('{}')
    return d


def test_latest_any_picks_newest(tmp_path: Path):
    _make_execution(tmp_path, "old")
    import time; time.sleep(0.01)
    _make_execution(tmp_path, "newer")
    eid, _ = resolve_execution(tmp_path, mode=RESOLVE_LATEST_ANY)
    assert eid == "newer"


def test_latest_complete_requires_evidence_manifest(tmp_path: Path):
    _make_execution(tmp_path, "complete", has_evidence=True)
    import time; time.sleep(0.01)
    _make_execution(tmp_path, "partial")
    eid, _ = resolve_execution(tmp_path, mode=RESOLVE_LATEST_COMPLETE)
    assert eid == "complete"


def test_latest_complete_returns_unknown_when_none_have_manifest(tmp_path: Path):
    _make_execution(tmp_path, "a")
    _make_execution(tmp_path, "b")
    eid, _ = resolve_execution(tmp_path, mode=RESOLVE_LATEST_COMPLETE)
    assert eid == "unknown"


def test_latest_judge_requires_judge_result(tmp_path: Path):
    _make_execution(tmp_path, "with-judge", has_judge=True)
    import time; time.sleep(0.01)
    _make_execution(tmp_path, "no-judge")
    eid, _ = resolve_execution(tmp_path, mode=RESOLVE_LATEST_JUDGE)
    assert eid == "with-judge"


def test_latest_judge_returns_unknown_when_none_have_judge(tmp_path: Path):
    _make_execution(tmp_path, "a")
    _make_execution(tmp_path, "b")
    eid, _ = resolve_execution(tmp_path, mode=RESOLVE_LATEST_JUDGE)
    assert eid == "unknown"


def test_latest_runtime_requires_runtime_manifest(tmp_path: Path):
    _make_execution(tmp_path, "with-rt", has_runtime=True)
    import time; time.sleep(0.01)
    _make_execution(tmp_path, "no-rt")
    eid, _ = resolve_execution(tmp_path, mode=RESOLVE_LATEST_RUNTIME)
    assert eid == "with-rt"


def test_latest_does_not_pick_partial_readiness_when_judge_needed(tmp_path: Path):
    _make_execution(tmp_path, "partial-readiness")
    import time; time.sleep(0.01)
    _make_execution(tmp_path, "full", has_evidence=True, has_judge=True)
    eid, _ = resolve_execution(tmp_path, mode=RESOLVE_LATEST_COMPLETE)
    assert eid == "full"


def test_latest_returns_unknown_on_empty_dir(tmp_path: Path):
    eid, _ = resolve_execution(tmp_path, mode=RESOLVE_LATEST_ANY)
    assert eid == "unknown"


def test_format_resolved_shows_path(tmp_path: Path):
    output = format_resolved("exec-001", tmp_path / ".aeos" / "evidence" / "exec-001")
    assert "exec-001" in output
    assert ".aeos" in output


def test_format_resolved_unknown():
    output = format_resolved("unknown", Path("/tmp/.aeos/evidence"))
    assert "unknown" in output


def test_normalize_mode_aliases():
    assert normalize_mode("latest") == RESOLVE_LATEST_COMPLETE
    assert normalize_mode(RESOLVE_LATEST_ANY) == RESOLVE_LATEST_ANY
