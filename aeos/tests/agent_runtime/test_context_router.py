from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.agent_runtime.context_router import ContextRouter


class TestContextRouter:
    def setup_method(self):
        self.router = ContextRouter()

    def test_build_context_packet(self):
        task = {
            "task_id": "task-001",
            "assigned_agent": "architect",
            "required_lcps": ["global-rules"],
            "scope": {"target": "."},
            "required_context": ["file1.md", "file2.md"],
            "required_evidence": ["ev-001"],
            "forbidden_actions": ["shell.run"],
            "quality_gates": ["facts_cite_evidence"],
        }
        packet = self.router.build_context_packet("exec-001", task)
        assert packet["context_id"] == "exec-001:task-001"
        assert packet["agent_id"] == "architect"
        assert len(packet["loaded_lcps"]) > 0
        assert len(packet["file_refs"]) == 2
        assert "shell.run" in packet["forbidden_actions"]

    def test_build_context_without_lcp_resolver(self):
        task = {
            "task_id": "task-002",
            "assigned_agent": "coder",
            "required_lcps": ["nonexistent-lcp"],
            "scope": {},
        }
        packet = self.router.build_context_packet("exec-002", task)
        assert packet["context_id"] == "exec-002:task-002"
        assert len(packet["loaded_lcps"]) == 1
        assert packet["loaded_lcps"][0]["resolved"] is False

    def test_limit_context(self):
        large_context = {
            "loaded_lcps": [{"id": f"lcp-{i}"} for i in range(20)],
            "file_refs": [f"file-{i}.md" for i in range(30)],
            "evidence_refs": [f"ev-{i}" for i in range(50)],
            "other": "data",
        }
        limited = self.router.limit_context(large_context)
        assert len(limited["loaded_lcps"]) <= 5
        assert len(limited["file_refs"]) <= 10
        assert len(limited["evidence_refs"]) <= 20
        assert limited["other"] == "data"

    def test_empty_context_packet(self):
        task = {"task_id": "", "assigned_agent": ""}
        packet = self.router.build_context_packet("exec-003", task)
        assert packet is not None
        assert packet["context_id"] == "exec-003:"
