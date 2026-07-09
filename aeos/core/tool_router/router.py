from __future__ import annotations

from pathlib import Path
from time import monotonic
from typing import Any, Optional

from aeos.core.governance.governance_gate import GovernanceGate
from aeos.core.governance.governance_models import (
    GOV_STATUS_BLOCKED,
    GOV_STATUS_PASS,
    GOV_STATUS_WAITING_APPROVAL,
    GovernanceRequest,
)
from aeos.core.evidence.evidence_store import EvidenceStore
from aeos.core.tool_router.adapters.base_adapter import BaseToolAdapter
from aeos.core.tool_router.tool_decision import make_decision
from aeos.core.tool_router.tool_models import ToolRequest, ToolResult, ToolRegistryConfig
from aeos.core.tool_router.tool_registry_loader import ToolRegistryLoader


ADAPTER_MAP: dict[str, type[BaseToolAdapter]] = {}


def register_adapter(tool_id: str, adapter_cls: type[BaseToolAdapter]):
    ADAPTER_MAP[tool_id] = adapter_cls


class ToolRouter:
    def __init__(
        self,
        workspace_root: str = ".",
        governance_gate: Optional[GovernanceGate] = None,
        evidence_store: Optional[EvidenceStore] = None,
    ):
        self.workspace_root = Path(workspace_root)
        self.governance_gate = governance_gate or GovernanceGate(str(self.workspace_root))
        self.evidence_store = evidence_store or EvidenceStore()
        self.registry_loader = ToolRegistryLoader(str(self.workspace_root))
        self.registry_config: Optional[ToolRegistryConfig] = None
        self._adapters: dict[str, BaseToolAdapter] = {}
        self._decisions: list = []
        self._results: list[ToolResult] = []

    def initialize(self) -> None:
        self.registry_config = self.registry_loader.load()
        self.governance_gate.initialize()
        self._register_builtin_adapters()

    @staticmethod
    def _register_builtin_adapters():
        from aeos.core.tool_router.adapters.filesystem_readonly_adapter import FilesystemReadonlyAdapter
        from aeos.core.tool_router.adapters.filesystem_sandbox_write_adapter import FilesystemSandboxWriteAdapter
        from aeos.core.tool_router.adapters.package_local_adapter import PackageLocalAdapter
        from aeos.core.tool_router.adapters.test_runner_mock_adapter import TestRunnerMockAdapter
        register_adapter("filesystem-readonly", FilesystemReadonlyAdapter)
        register_adapter("filesystem-write-sandbox", FilesystemSandboxWriteAdapter)
        register_adapter("package-local", PackageLocalAdapter)
        register_adapter("test-runner-controlled", TestRunnerMockAdapter)

    def register_adapter_instance(self, tool_id: str, adapter: BaseToolAdapter):
        self._adapters[tool_id] = adapter

    def route(self, request: ToolRequest) -> ToolResult:
        started = monotonic()
        registry = self.registry_config

        tool_entry = self._find_tool(request.tool_id)
        if not tool_entry:
            return self._build_result(request, "BLOCKED", error=f"Unknown tool_id: {request.tool_id}", duration_ms=0)

        gov_req = self._build_governance_request(request)
        gov_result = self.governance_gate.evaluate(gov_req)

        perm_decision_id = gov_result.permission_decision_id
        pol_decision_id = gov_result.policy_decision_id

        if gov_result.status == GOV_STATUS_BLOCKED:
            decision = make_decision(
                execution_id=request.execution_id,
                request_id=request.request_id,
                tool_id=request.tool_id,
                action=request.action,
                status="BLOCKED",
                permission_allowed=gov_result.permission_allowed,
                policy_allowed=gov_result.policy_allowed,
                governance_status=gov_result.status,
                reason=gov_result.blocking_reason or "Governance gate blocked",
                permission_decision_id=perm_decision_id,
                policy_decision_id=pol_decision_id,
                evidence_refs=gov_result.evidence_refs,
            )
            self._decisions.append(decision)
            self.evidence_store.store_record(request.execution_id, "tool_decision", decision.to_dict())
            result = self._build_result(request, "BLOCKED", error=gov_result.blocking_reason, duration_ms=0)
            result.permission_decision_id = perm_decision_id
            result.policy_decision_id = pol_decision_id
            result.governance_status = gov_result.status
            result.evidence_refs = gov_result.evidence_refs
            self._results.append(result)
            self.evidence_store.store_record(request.execution_id, "tool_result", result.to_dict())
            return result

        if gov_result.status == GOV_STATUS_WAITING_APPROVAL:
            decision = make_decision(
                execution_id=request.execution_id,
                request_id=request.request_id,
                tool_id=request.tool_id,
                action=request.action,
                status="WAITING_APPROVAL",
                permission_allowed=gov_result.permission_allowed,
                policy_allowed=gov_result.policy_allowed,
                governance_status=gov_result.status,
                reason=gov_result.blocking_reason or "Waiting approval",
                permission_decision_id=perm_decision_id,
                policy_decision_id=pol_decision_id,
                evidence_refs=gov_result.evidence_refs,
            )
            self._decisions.append(decision)
            self.evidence_store.store_record(request.execution_id, "tool_decision", decision.to_dict())
            result = self._build_result(request, "WAITING_APPROVAL", error=gov_result.blocking_reason, duration_ms=0)
            result.permission_decision_id = perm_decision_id
            result.policy_decision_id = pol_decision_id
            result.governance_status = gov_result.status
            result.evidence_refs = gov_result.evidence_refs
            self._results.append(result)
            self.evidence_store.store_record(request.execution_id, "tool_result", result.to_dict())
            return result

        adapter = self._get_adapter(request.tool_id)
        if not adapter:
            decision = make_decision(
                execution_id=request.execution_id,
                request_id=request.request_id,
                tool_id=request.tool_id,
                action=request.action,
                status="ERROR",
                permission_allowed=True,
                policy_allowed=True,
                governance_status=gov_result.status,
                reason=f"No adapter registered for tool_id: {request.tool_id}",
                permission_decision_id=perm_decision_id,
                policy_decision_id=pol_decision_id,
                evidence_refs=gov_result.evidence_refs,
            )
            self._decisions.append(decision)
            self.evidence_store.store_record(request.execution_id, "tool_decision", decision.to_dict())
            result = self._build_result(request, "ERROR", error=f"No adapter for tool_id: {request.tool_id}", duration_ms=0)
            result.permission_decision_id = perm_decision_id
            result.policy_decision_id = pol_decision_id
            result.governance_status = gov_result.status
            result.evidence_refs = gov_result.evidence_refs
            self._results.append(result)
            self.evidence_store.store_record(request.execution_id, "tool_result", result.to_dict())
            return result

        try:
            output = adapter.execute(request.action, request.resource, request.input)
            duration_ms = int((monotonic() - started) * 1000)
            decision = make_decision(
                execution_id=request.execution_id,
                request_id=request.request_id,
                tool_id=request.tool_id,
                action=request.action,
                status="PASS",
                permission_allowed=True,
                policy_allowed=True,
                governance_status=gov_result.status,
                reason="Tool executed successfully",
                permission_decision_id=perm_decision_id,
                policy_decision_id=pol_decision_id,
                evidence_refs=gov_result.evidence_refs,
            )
            self._decisions.append(decision)
            self.evidence_store.store_record(request.execution_id, "tool_decision", decision.to_dict())
            result = self._build_result(request, "PASS", output=output, duration_ms=duration_ms)
            result.permission_decision_id = perm_decision_id
            result.policy_decision_id = pol_decision_id
            result.governance_status = gov_result.status
            result.evidence_refs = gov_result.evidence_refs
            self._results.append(result)
            self.evidence_store.store_record(request.execution_id, "tool_result", result.to_dict())
            return result
        except Exception as e:
            duration_ms = int((monotonic() - started) * 1000)
            decision = make_decision(
                execution_id=request.execution_id,
                request_id=request.request_id,
                tool_id=request.tool_id,
                action=request.action,
                status="ERROR",
                permission_allowed=True,
                policy_allowed=True,
                governance_status=gov_result.status,
                reason=f"Adapter execution error: {e}",
                permission_decision_id=perm_decision_id,
                policy_decision_id=pol_decision_id,
                evidence_refs=gov_result.evidence_refs,
            )
            self._decisions.append(decision)
            self.evidence_store.store_record(request.execution_id, "tool_decision", decision.to_dict())
            result = self._build_result(request, "ERROR", error=str(e), duration_ms=duration_ms)
            result.permission_decision_id = perm_decision_id
            result.policy_decision_id = pol_decision_id
            result.governance_status = gov_result.status
            result.evidence_refs = gov_result.evidence_refs
            self._results.append(result)
            self.evidence_store.store_record(request.execution_id, "tool_result", result.to_dict())
            return result

    def _find_tool(self, tool_id: str) -> dict[str, Any] | None:
        if not self.registry_config:
            return None
        for mcp in self.registry_config.mcps:
            if mcp.get("id") == tool_id:
                return mcp
        return None

    def _build_governance_request(self, request: ToolRequest) -> GovernanceRequest:
        from aeos.core.governance.governance_models import GovernanceRequest as GR
        return GR(
            execution_id=request.execution_id,
            actor=request.actor,
            role=request.role,
            action=request.action,
            capability=request.capability,
            resource=request.resource,
            command=request.command,
            branch=request.branch,
            approval_present=request.approval_id is not None,
            details=request.details,
        )

    def _get_adapter(self, tool_id: str) -> BaseToolAdapter | None:
        if tool_id in self._adapters:
            return self._adapters[tool_id]
        if tool_id in ADAPTER_MAP:
            cls = ADAPTER_MAP[tool_id]
            instance = cls()
            self._adapters[tool_id] = instance
            return instance
        return None

    def _build_result(self, request: ToolRequest, status: str, output: dict | None = None, error: str | None = None, duration_ms: int = 0) -> ToolResult:
        return ToolResult(
            execution_id=request.execution_id,
            request_id=request.request_id,
            tool_id=request.tool_id,
            action=request.action,
            status=status,
            output=output or {},
            error=error,
            duration_ms=duration_ms,
        )

    def get_decisions(self) -> list:
        return list(self._decisions)

    def get_results(self) -> list[ToolResult]:
        return list(self._results)

    def generate_report(self) -> str:
        from aeos.core.tool_router.tool_reporter import ToolRouterReporter
        config_info = None
        if self.registry_config:
            config_info = {
                "tool_router_enabled": self.registry_config.tool_router_config.get("tool_router", {}).get("enabled", False),
                "mcp_runtime_enabled": self.registry_config.mcp_runtime_config.get("mcp_runtime", {}).get("enabled", False),
                "fail_closed": self.registry_config.tool_router_config.get("tool_router", {}).get("fail_closed", True),
                "mcps_count": len(self.registry_config.mcps),
                "loaded_files": self.registry_config.loaded_files,
                "findings_count": len(self.registry_config.findings),
            }
        reporter = ToolRouterReporter()
        execution_id = self._results[0].execution_id if self._results else "unknown"
        return reporter.generate_report(execution_id, self._decisions, self._results, config_info)
