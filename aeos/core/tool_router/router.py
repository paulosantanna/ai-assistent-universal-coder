"""AEOS Tool Router — controlled routing layer with permission, policy, MCP, redaction and evidence."""

from __future__ import annotations

from dataclasses import asdict
from time import monotonic
from .contracts import ToolCallRequest, ToolCallResult


class ToolRouter:
    def __init__(self, permission_engine, policy_engine, mcp_registry, mcp_runtime, evidence_store, redactor):
        self.permission_engine = permission_engine
        self.policy_engine = policy_engine
        self.mcp_registry = mcp_registry
        self.mcp_runtime = mcp_runtime
        self.evidence_store = evidence_store
        self.redactor = redactor

    def call(self, request: ToolCallRequest) -> ToolCallResult:
        started = monotonic()
        req_dict = asdict(request)

        permission = self.permission_engine.decide(req_dict)
        self.evidence_store.write_permission_decision(request.execution_id, req_dict, permission)
        if not permission.get("allowed", False):
            return self._blocked(request, started, permission, {}, "permission_denied")

        policy = self.policy_engine.decide(req_dict)
        self.evidence_store.write_policy_decision(request.execution_id, req_dict, policy)
        if not policy.get("allowed", False):
            return self._blocked(request, started, permission, policy, "policy_denied")

        mcp = self.mcp_registry.resolve(request.mcp_id)
        if not mcp:
            return self._blocked(request, started, permission, policy, "mcp_not_registered")

        if not self.mcp_registry.is_tool_allowed(request.mcp_id, request.tool_name):
            return self._blocked(request, started, permission, policy, "tool_not_allowlisted")

        try:
            raw = self.mcp_runtime.invoke(request)
            safe_output, redact_findings = self.redactor.redact(raw)
            result = ToolCallResult(
                request_id=request.request_id,
                status="success",
                output=safe_output,
                redacted=len(redact_findings) > 0,
                duration_ms=int((monotonic() - started) * 1000),
                permission_decision=permission,
                policy_decision=policy,
            )
            self.evidence_store.write_tool_call(request.execution_id, req_dict, asdict(result))
            self.evidence_store.write_mcp_call(request.execution_id, request.mcp_id, request.tool_name, dict(request.input), raw)
            return result
        except TimeoutError as exc:
            return self._failed(request, started, permission, policy, "timeout", exc)
        except Exception as exc:
            return self._failed(request, started, permission, policy, "failed", exc)

    def _blocked(self, request, started, permission, policy, reason):
        result = ToolCallResult(
            request_id=request.request_id,
            status="blocked",
            duration_ms=int((monotonic() - started) * 1000),
            permission_decision=permission,
            policy_decision=policy,
            errors=[reason],
        )
        self.evidence_store.write_tool_call(request.execution_id, asdict(request), asdict(result))
        return result

    def _failed(self, request, started, permission, policy, status, exc):
        result = ToolCallResult(
            request_id=request.request_id,
            status="timeout" if status == "timeout" else "failed",
            duration_ms=int((monotonic() - started) * 1000),
            permission_decision=permission,
            policy_decision=policy,
            errors=[str(exc)],
        )
        self.evidence_store.write_tool_call(request.execution_id, asdict(request), asdict(result))
        return result