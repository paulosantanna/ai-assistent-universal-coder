from __future__ import annotations

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.evals.eval_suite_loader import EvalSuiteLoader


class TestEvalSuiteLoader:
    def setup_method(self):
        self.loader = EvalSuiteLoader(workspace_root=".")

    def test_loads_suites(self):
        suites = self.loader.load_all()
        assert len(suites) > 0
        suite_ids = [s.suite_id for s in suites]
        assert "anti_hallucination" in suite_ids
        assert "evidence_integrity" in suite_ids
        assert "secret_redaction" in suite_ids
        assert "package_security" in suite_ids

    def test_loads_cases_for_suites(self):
        suites = self.loader.load_all()
        for suite in suites:
            if suite.suite_id == "anti_hallucination":
                assert len(suite.cases) > 0
                break

    def test_load_by_id(self):
        suite = self.loader.load_by_id("secret_redaction")
        assert suite is not None
        assert suite.suite_id == "secret_redaction"

    def test_load_unknown_suite_returns_none(self):
        suite = self.loader.load_by_id("nonexistent-suite")
        assert suite is None

    def test_list_suites(self):
        self.loader.load_all()
        listings = self.loader.list_suites()
        assert len(listings) > 0
        assert any(l["id"] == "package_security" for l in listings)
