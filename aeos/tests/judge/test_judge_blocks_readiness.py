from __future__ import annotations

import sys
import os
import json
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.judge.judge_models import JudgeResult, JUDGE_STATUS_PASS, JUDGE_STATUS_BLOCKED
from aeos.core.readiness.readiness_auditor import ReadinessAuditor
from aeos.core.readiness.readiness_models import READINESS_PASS, READINESS_BLOCKED


class TestJudgeBlocksReadiness:
    def test_judge_blocked_equals_not_pass(self):
        assert JUDGE_STATUS_BLOCKED != JUDGE_STATUS_PASS

    def test_readiness_blocked_when_judge_blocked_via_critical_blockers(self):
        auditor = ReadinessAuditor(workspace_root=".")
        result = auditor.audit()
        has_blocked_text = any("BLOCKED" in cb for cb in result.critical_blockers)
        has_judge_text = any("Judge" in cb for cb in result.critical_blockers)
        if has_judge_text:
            assert result.status != READINESS_PASS, "Readiness cannot PASS when Judge is BLOCKED"
