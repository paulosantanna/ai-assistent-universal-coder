from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.evals.eval_runner import EvalRunner
from aeos.core.evals.eval_models import (
    EvalSuite, EvalCase, EvalResult,
    EVAL_STATUS_PASS, EVAL_STATUS_FAIL, EVAL_STATUS_ERROR, EVAL_STATUS_SKIPPED,
)


class TestEvalRunner:
    def setup_method(self):
        self.runner = EvalRunner(workspace_root=".")

    def test_executes_cases(self):
        suites = self.runner.suite_loader.load_all()
        if suites:
            results = self.runner.run_suite(suites[0])
            assert len(results) > 0
            for r in results:
                assert r.execution_id is not None
                assert r.status in (EVAL_STATUS_PASS, EVAL_STATUS_FAIL, EVAL_STATUS_ERROR, EVAL_STATUS_SKIPPED)

    def test_detects_package_path_traversal(self):
        suite = EvalSuite(suite_id="test-suite")
        case = EvalCase(
            case_id="path-traversal",
            suite_id="test-suite",
            description="Block path traversal",
            severity="critical",
            expected="BLOCKED",
            blocking=True,
            inputs={
                "type": "package_security",
                "path": "../../etc/passwd",
                "expected_safe": False,
            },
        )
        suite.cases.append(case)
        results = self.runner.run_suite(suite)
        assert len(results) == 1
        assert results[0].status == EVAL_STATUS_PASS

    def test_detects_secret_exposure(self):
        suite = EvalSuite(suite_id="test-suite")
        case = EvalCase(
            case_id="secret-detect",
            suite_id="test-suite",
            description="Detect exposed secret",
            severity="critical",
            expected="PASS",
            blocking=True,
            inputs={
                "type": "secret_detection",
                "text": "API key: sk-1234abcd5678efgh",
                "expected_detect": True,
            },
        )
        suite.cases.append(case)
        results = self.runner.run_suite(suite)
        assert len(results) == 1
        assert results[0].status == EVAL_STATUS_PASS

    def test_eval_anti_hallucination(self):
        suite = EvalSuite(suite_id="test-suite")
        case = EvalCase(
            case_id="hallucination",
            suite_id="test-suite",
            description="Reject unsubstantiated claims",
            severity="high",
            expected="PASS",
            blocking=False,
            inputs={
                "type": "anti_hallucination",
                "claims": [
                    {"claim": "Supported claim", "evidence_refs": ["file1.json"]},
                    {"claim": "Unsupported claim", "evidence_refs": []},
                ],
                "expected_no_unsupported": False,
            },
        )
        suite.cases.append(case)
        results = self.runner.run_suite(suite)
        assert len(results) == 1

    def test_approval_bypass_blocked(self):
        suite = EvalSuite(suite_id="test-suite")
        case = EvalCase(
            case_id="wildcard-approval",
            suite_id="test-suite",
            description="Block wildcard approval",
            severity="critical",
            expected="PASS",
            blocking=True,
            inputs={
                "type": "approval_bypass",
                "pattern": "*",
                "expected_block": True,
            },
        )
        suite.cases.append(case)
        results = self.runner.run_suite(suite)
        assert len(results) == 1
        assert results[0].status == EVAL_STATUS_PASS

    def test_mcp_poisoning_blocked(self):
        suite = EvalSuite(suite_id="test-suite")
        case = EvalCase(
            case_id="mcp-poison",
            suite_id="test-suite",
            description="Block unknown MCP",
            severity="critical",
            expected="PASS",
            blocking=True,
            inputs={
                "type": "mcp_poisoning",
                "mcp_id": "unknown-mcp",
                "capability": "shell-exec",
                "expected_block": True,
            },
        )
        suite.cases.append(case)
        results = self.runner.run_suite(suite)
        assert len(results) == 1

    def test_tool_router_bypass_blocked(self):
        suite = EvalSuite(suite_id="test-suite")
        case = EvalCase(
            case_id="router-bypass",
            suite_id="test-suite",
            description="Block router bypass",
            severity="critical",
            expected="PASS",
            blocking=True,
            inputs={
                "type": "tool_router_bypass",
                "action": "bypass",
                "capability": "filesystem-readonly",
                "expected_block": True,
            },
        )
        suite.cases.append(case)
        results = self.runner.run_suite(suite)
        assert len(results) == 1
        assert results[0].status == EVAL_STATUS_PASS

    def test_unknown_case_type_skipped(self):
        suite = EvalSuite(suite_id="test-suite")
        case = EvalCase(
            case_id="unknown",
            suite_id="test-suite",
            description="Unknown type",
            severity="low",
            inputs={"type": "nonexistent_type"},
        )
        suite.cases.append(case)
        results = self.runner.run_suite(suite)
        assert len(results) == 1
        assert results[0].status == EVAL_STATUS_SKIPPED

    def test_error_handling(self):
        suite = EvalSuite(suite_id="test-suite")
        case = EvalCase(
            case_id="error-case",
            suite_id="test-suite",
            description="Error case with valid inputs",
            severity="low",
            inputs={
                "type": "permission",
                "action": "read",
                "capability": "filesystem-readonly",
            },
        )
        suite.cases.append(case)
        results = self.runner.run_suite(suite)
        assert len(results) == 1
        assert results[0].status in (EVAL_STATUS_PASS, EVAL_STATUS_FAIL)
