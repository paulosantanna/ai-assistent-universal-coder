from __future__ import annotations

from lsprotocol.types import Position, Range

from aeos_lsp.semantic.models import (
    Agent, AgentLayer, Skill, Playbook, PlaybookStep, Tool, Command,
    Policy, Permission, Registry, ModelProfile, TokenBudget, QualityGate,
    JudgeRule, EvidenceRequirement, Artifact, Variable, Input, Output,
    Dependency, ExecutionTarget, ApprovalRequirement, RollbackDefinition,
    SymbolKind, Visibility, DeprecationStatus, Workspace, Repository,
)

A_RANGE = Range(start=Position(line=0, character=0), end=Position(line=1, character=0))


class TestAgent:
    def test_agent_creation(self, sample_agent_symbol):
        assert sample_agent_symbol.stable_id == "agent:test-agent"
        assert sample_agent_symbol.name == "test-agent"
        assert sample_agent_symbol.parent_id == "base-agent"
        assert len(sample_agent_symbol.layers) == 1

    def test_agent_layer(self, sample_agent_symbol):
        layer = sample_agent_symbol.layers[0]
        assert layer.name == "reasoning"
        assert layer.skills == ["analysis-skill"]

    def test_agent_kind(self, sample_agent_symbol):
        assert sample_agent_symbol.symbol_kind == SymbolKind.AGENT

    def test_agent_deprecation(self):
        agent = Agent(
            stable_id="agent:old", name="old",
            source_uri="file:///old.yaml",
            selection_range=A_RANGE, full_range=A_RANGE,
            deprecation=DeprecationStatus.DEPRECATED,
        )
        assert agent.deprecation == DeprecationStatus.DEPRECATED

    def test_agent_visibility_private(self):
        agent = Agent(
            stable_id="agent:private", name="private",
            source_uri="file:///private.yaml",
            selection_range=A_RANGE, full_range=A_RANGE,
            visibility=Visibility.PRIVATE,
        )
        assert agent.visibility == Visibility.PRIVATE


class TestSkill:
    def test_skill_creation(self, sample_skill_symbol):
        assert sample_skill_symbol.name == "test-skill"
        assert "file-reader" in sample_skill_symbol.tools
        assert "query" in sample_skill_symbol.inputs

    def test_skill_kind(self, sample_skill_symbol):
        assert sample_skill_symbol.symbol_kind == SymbolKind.SKILL


class TestPlaybook:
    def test_playbook_creation(self, sample_playbook_symbol):
        assert sample_playbook_symbol.name == "test-playbook"
        assert sample_playbook_symbol.symbol_kind == SymbolKind.PLAYBOOK


class TestPlaybookStep:
    def test_step_creation(self):
        step = PlaybookStep(
            stable_id="step:gather-data",
            name="gather-data",
            step_type="tool",
            tool="data-collector",
            inputs={"source": "api"},
            outputs={"raw": "data"},
            source_uri="file:///playbook.yaml",
        )
        assert step.tool == "data-collector"

    def test_step_with_conditions(self):
        step = PlaybookStep(
            stable_id="step:conditional", name="conditional",
            conditions=["x > 5"], source_uri="file:///p.yaml",
        )
        assert "x > 5" in step.conditions

    def test_step_with_timeout(self):
        step = PlaybookStep(
            stable_id="step:timed", name="timed",
            tool="runner", timeout=60, retry=3,
            source_uri="file:///p.yaml",
        )
        assert step.timeout == 60
        assert step.retry == 3


class TestTool:
    def test_tool_creation(self):
        tool = Tool(
            stable_id="tool:file-reader",
            name="file-reader",
            command=Command(
                stable_id="cmd:read-file", name="read-file",
                args=["path"], mutating=False,
            ),
            mutating=False,
            timeout=30,
            source_uri="file:///tool.yaml",
        )
        assert tool.name == "file-reader"
        assert tool.command.name == "read-file"
        assert not tool.mutating
        assert tool.timeout == 30

    def test_tool_kind(self):
        tool = Tool(
            stable_id="tool:test", name="test",
            source_uri="file:///t.yaml",
        )
        assert tool.symbol_kind == SymbolKind.TOOL

    def test_tool_mutating(self):
        tool = Tool(
            stable_id="tool:writer", name="writer",
            source_uri="file:///w.yaml", mutating=True,
        )
        assert tool.mutating


class TestCommand:
    def test_command_creation(self):
        cmd = Command(
            stable_id="cmd:python", name="python",
            args=["script.py", "--verbose"],
        )
        assert cmd.name == "python"
        assert cmd.args == ["script.py", "--verbose"]

    def test_command_minimal(self):
        cmd = Command(stable_id="cmd:ls", name="ls")
        assert cmd.args == []


class TestPolicy:
    def test_policy_creation(self):
        policy = Policy(
            stable_id="policy:approval",
            name="approval-required",
            rules={"require_approval": True},
            source_uri="file:///policies.yaml",
        )
        assert policy.rules["require_approval"] is True


class TestPermission:
    def test_permission_creation(self):
        perm = Permission(
            stable_id="permission:read-only",
            name="read-only",
            scopes=["workspace:read"],
            capabilities=["file:read"],
            source_uri="file:///permissions.yaml",
        )
        assert "workspace:read" in perm.scopes


class TestRegistry:
    def test_registry_creation(self):
        reg = Registry(
            stable_id="registry:agents",
            name="agents",
            entries={"test-agent": {"ref": "agent:test-agent"}},
            registry_type="agents",
            source_uri="file:///agents.registry.yaml",
        )
        assert reg.entries["test-agent"]["ref"] == "agent:test-agent"


class TestVariable:
    def test_variable_creation(self):
        var = Variable(
            stable_id="var:threshold",
            name="threshold",
            source_uri="file:///vars.yaml",
            type_ref="integer",
            default=42,
        )
        assert var.type_ref == "integer"
        assert var.default == 42


class TestInputOutput:
    def test_input_creation(self):
        inp = Input(
            stable_id="input:query", name="query",
            source_uri="file:///input.yaml",
            type_ref="string", required=True,
        )
        assert inp.type_ref == "string"
        assert inp.required

    def test_output_creation(self):
        out = Output(
            stable_id="output:result", name="result",
            source_uri="file:///output.yaml", type_ref="json",
        )
        assert out.type_ref == "json"


class TestWorkspace:
    def test_workspace_creation(self):
        ws = Workspace(
            stable_id="workspace:root",
            name="AEOS Workspace",
            folders=["file:///folder1", "file:///folder2"],
        )
        assert len(ws.folders) == 2
        assert ws.symbol_kind == SymbolKind.WORKSPACE


class TestRepository:
    def test_repository_creation(self):
        repo = Repository(stable_id="repo:main", name="main", uri="file:///workspace")
        assert repo.symbol_kind == SymbolKind.REPOSITORY


class TestSymbolKind:
    def test_symbol_kind_values(self):
        assert SymbolKind.AGENT.value == "agent"
        assert SymbolKind.SKILL.value == "skill"
        assert SymbolKind.WORKSPACE.value == "workspace"
        assert SymbolKind.LAYER.value == "layer"


class TestVisibility:
    def test_visibility_values(self):
        assert Visibility.PUBLIC.value == "public"
        assert Visibility.PRIVATE.value == "private"
        assert Visibility.INTERNAL.value == "internal"


class TestDeprecationStatus:
    def test_deprecation_values(self):
        assert DeprecationStatus.CURRENT.value == "current"
        assert DeprecationStatus.DEPRECATED.value == "deprecated"


class TestAgentLayer:
    def test_layer_creation(self):
        layer = AgentLayer(
            stable_id="agent:test/layer:code",
            name="code",
            skills=["python", "typescript"],
        )
        assert layer.symbol_kind == SymbolKind.LAYER

    def test_layer_kind_constant(self):
        layer = AgentLayer(stable_id="a:b", name="b")
        assert layer.symbol_kind == SymbolKind.LAYER


class TestQualityGate:
    def test_quality_gate_creation(self):
        qg = QualityGate(
            stable_id="gate:test", name="test-gate",
            rules={"min_coverage": 80},
            source_uri="file:///quality.yaml",
        )
        assert qg.rules["min_coverage"] == 80


class TestModelProfile:
    def test_model_profile_creation(self):
        mp = ModelProfile(
            stable_id="profile:test", name="test-profile",
            provider="openai",
            source_uri="file:///profile.yaml",
        )
        assert mp.provider == "openai"


class TestTokenBudget:
    def test_token_budget_creation(self):
        tb = TokenBudget(
            stable_id="budget:test", name="test-budget",
            max_input_tokens=100000,
            source_uri="file:///budget.yaml",
        )
        assert tb.max_input_tokens == 100000


class TestJudgeRule:
    def test_judge_rule_creation(self):
        jr = JudgeRule(
            stable_id="judge:test", name="test-judge",
            min_score=9.0, source_uri="file:///judge.yaml",
        )
        assert jr.min_score == 9.0


class TestEvidenceRequirement:
    def test_evidence_requirement_creation(self):
        er = EvidenceRequirement(
            stable_id="evidence:test", name="test-evidence",
            required_evidence=["hash", "signature"],
            source_uri="file:///evidence.yaml",
        )
        assert "hash" in er.required_evidence


class TestArtifact:
    def test_artifact_creation(self):
        art = Artifact(
            stable_id="artifact:test-output", name="test-output",
            source_uri="file:///artifact.yaml",
            kind="output",
        )
        assert art.kind == "output"


class TestDependency:
    def test_dependency_creation(self):
        dep = Dependency(
            stable_id="dep:test",
            source_id="skill:analysis",
            target_id="tool:data-collector",
            source_uri="file:///dep.yaml",
        )
        assert dep.source_id == "skill:analysis"
        assert dep.target_id == "tool:data-collector"


class TestExecutionTarget:
    def test_execution_target_creation(self):
        et = ExecutionTarget(
            stable_id="target:test", name="test-target",
            executor="agent:test-agent",
            source_uri="file:///target.yaml",
        )
        assert et.executor == "agent:test-agent"


class TestApprovalRequirement:
    def test_approval_requirement_creation(self):
        ar = ApprovalRequirement(
            stable_id="approval:test", name="test-approval",
            required_approvals=2,
            source_uri="file:///approval.yaml",
        )
        assert ar.required_approvals == 2


class TestRollbackDefinition:
    def test_rollback_definition_creation(self):
        rd = RollbackDefinition(
            stable_id="rollback:test", name="test-rollback",
            steps=["step:revert-db", "step:clean-temp"],
            source_uri="file:///rollback.yaml",
        )
        assert len(rd.steps) == 2

    def test_rollback_with_strategy(self):
        rd = RollbackDefinition(
            stable_id="rollback:parallel", name="parallel-rollback",
            steps=["step:a", "step:b"],
            strategy="parallel",
            source_uri="file:///r.yaml",
        )
        assert rd.strategy == "parallel"
