from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from aeos.core.agent_runtime.agent_runtime import AgentRuntime
from aeos.core.agent_runtime.agent_models import AgentTask, generate_task_id
from aeos.core.agent_runtime.message_bus import MessageBus
from aeos.core.agent_runtime.trace_store import AgentTraceStore
from aeos.core.evidence.evidence_store import EvidenceStore


class TestAgentRuntime:
    def setup_method(self):
        self.runtime = AgentRuntime(workspace_root=".")
        self.evidence = EvidenceStore()
        self.message_bus = MessageBus()
        self.trace_store = AgentTraceStore(".")

    def test_execute_known_agent(self):
        task = AgentTask(
            execution_id="test-agent-exec",
            task_id=generate_task_id(),
            agent_id="root",
            actor="tester",
            role="tester",
            objective="Test agent execution",
        )
        result = self.runtime.execute_task(task)
        assert result.status in ("PASS", "BLOCKED")

    def test_execute_unknown_agent(self):
        task = AgentTask(
            execution_id="test-unknown-agent",
            task_id=generate_task_id(),
            agent_id="nonexistent-agent",
            actor="tester",
            role="tester",
            objective="Test unknown agent",
        )
        result = self.runtime.execute_task(task)
        assert result.status == "BLOCKED"
        assert "agent" in str(result.blocking_conditions).lower()

    def test_registers_message_on_execution(self):
        task = AgentTask(
            execution_id="test-messages",
            task_id=generate_task_id(),
            agent_id="planner",
            actor="tester",
            role="tester",
            objective="Test messages",
        )
        result = self.runtime.execute_task(task)
        assert len(result.messages) > 0

    def test_delegation_blocks_nonexistent_agent(self):
        parent_task = AgentTask(
            execution_id="test-delegation-block",
            task_id=generate_task_id(),
            agent_id="root",
            actor="tester",
            role="tester",
            objective="Test delegation block",
        )
        result = self.runtime.delegate_task(parent_task, "nonexistent-agent", "test", {})
        assert result.status == "BLOCKED"

    def test_delegation_blocks_self_delegation(self):
        parent_task = AgentTask(
            execution_id="test-self-delegation",
            task_id=generate_task_id(),
            agent_id="root",
            actor="tester",
            role="tester",
            objective="Test self delegation",
        )
        result = self.runtime.delegate_task(parent_task, "root", "test", {})
        assert result.status == "BLOCKED"
        assert "cannot delegate to itself" in str(result.blocking_conditions)

    def test_delegation_blocks_self_judging(self):
        parent_task = AgentTask(
            execution_id="test-self-judge",
            task_id=generate_task_id(),
            agent_id="judge",
            actor="tester",
            role="tester",
            objective="Test self judge",
        )
        result = self.runtime.delegate_task(parent_task, "judge", "test", {})
        assert result.status == "BLOCKED"

    def test_finalize_execution(self):
        summary = self.runtime.finalize_execution("test-finalize")
        assert "execution_id" in summary
        assert "message_count" in summary
        assert "delegation_history" in summary
