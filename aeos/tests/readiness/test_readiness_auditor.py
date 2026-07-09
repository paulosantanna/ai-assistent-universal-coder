from __future__ import annotations

import sys
import os
import json
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.readiness.readiness_auditor import ReadinessAuditor, READINESS_CATEGORIES
from aeos.core.readiness.readiness_models import READINESS_PASS, READINESS_BLOCKED, READINESS_REVIEW


class TestReadinessAuditor:
    def setup_method(self):
        self.auditor = ReadinessAuditor(workspace_root=".")

    def test_audit_returns_result(self):
        result = self.auditor.audit()
        assert result.execution_id is not None
        assert result.status in (READINESS_PASS, READINESS_BLOCKED, READINESS_REVIEW)
        assert result.overall_score >= 0.0

    def test_audit_has_categories(self):
        result = self.auditor.audit()
        for cat in READINESS_CATEGORIES:
            assert cat in result.categories, f"Missing category: {cat}"
            assert 0.0 <= result.categories[cat] <= 1.0

    def test_audit_computes_score(self):
        result = self.auditor.audit()
        assert 0.0 <= result.overall_score <= 1.0

    def test_audit_generates_scorecard(self):
        result = self.auditor.audit()
        scorecard = self.auditor.get_scorecard()
        assert scorecard.execution_id == result.execution_id
        assert scorecard.overall_score == result.overall_score

    def test_critical_blockers(self):
        result = self.auditor.audit()
        assert isinstance(result.critical_blockers, list)
        assert isinstance(result.high_risks, list)
        assert isinstance(result.medium_risks, list)

    def test_blocks_when_judge_blocked(self):
        auditor = ReadinessAuditor(workspace_root=".")
        result = auditor.audit()
        if result.status == READINESS_PASS:
            import json
            judge_result = None
            evidence_root = Path(".aeos") / "evidence"
            if evidence_root.exists():
                dirs = sorted([d for d in evidence_root.iterdir() if d.is_dir()], key=lambda d: d.stat().st_mtime, reverse=True)
                for d in dirs:
                    fp = d / "judge-result.json"
                    if fp.exists():
                        try:
                            judge_result = json.loads(fp.read_text(encoding="utf-8"))
                        except (json.JSONDecodeError, IOError):
                            pass
                        break
            if judge_result and judge_result.get("status") == "BLOCKED":
                assert result.status == READINESS_BLOCKED, "Readiness should be BLOCKED when Judge is BLOCKED"
