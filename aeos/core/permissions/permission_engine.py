from __future__ import annotations

from aeos.core.permissions.capability_loader import CapabilityLoader
from aeos.core.permissions.permission_models import (
    PermissionConfig,
    PermissionDecision,
    PermissionRequest,
    generate_decision_id,
    now_iso,
)


class PermissionEngine:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = workspace_root
        self.loader = CapabilityLoader(workspace_root)
        self.config: PermissionConfig | None = None
        self.decisions: list[PermissionDecision] = []

    def initialize(self) -> None:
        self.config = self.loader.load()
        self.loader.load_capabilities_list()

    def evaluate(self, request: PermissionRequest) -> PermissionDecision:
        decision_id = generate_decision_id()
        now = now_iso()

        if not self.config:
            return PermissionDecision(
                decision_id=decision_id,
                execution_id=request.execution_id,
                actor=request.actor,
                role=request.role,
                action=request.action,
                capability=request.capability,
                resource=request.resource,
                allowed=False,
                requires_approval=False,
                approval_id=None,
                reason="Permission engine not initialized",
                timestamp=now,
            )

        if not request.role:
            return self._deny(request, decision_id, now, "Actor has no role assigned")

        role_mapping = self.config.roles.get(request.role)
        if not role_mapping:
            return self._deny(request, decision_id, now, f"Role '{request.role}' does not exist")

        if not request.capability:
            return self._deny(request, decision_id, now, "No capability specified")

        if not self.loader.is_known_capability(request.capability):
            return self._deny(request, decision_id, now, f"Capability '{request.capability}' does not exist")

        if request.capability not in role_mapping.capabilities:
            return self._deny(
                request, decision_id, now,
                f"Role '{request.role}' does not have capability '{request.capability}'",
            )

        requires_approval = request.action in self.config.approval_required_actions

        decision = PermissionDecision(
            decision_id=decision_id,
            execution_id=request.execution_id,
            actor=request.actor,
            role=request.role,
            action=request.action,
            capability=request.capability,
            resource=request.resource,
            allowed=True,
            requires_approval=requires_approval,
            approval_id=None,
            reason="Allowed by role capability mapping"
            if not requires_approval
            else "Action requires approval",
            timestamp=now,
        )

        self.decisions.append(decision)
        return decision

    def _deny(
        self, request: PermissionRequest, decision_id: str, timestamp: str, reason: str
    ) -> PermissionDecision:
        decision = PermissionDecision(
            decision_id=decision_id,
            execution_id=request.execution_id,
            actor=request.actor,
            role=request.role,
            action=request.action,
            capability=request.capability,
            resource=request.resource,
            allowed=False,
            requires_approval=False,
            approval_id=None,
            reason=reason,
            timestamp=timestamp,
        )
        self.decisions.append(decision)
        return decision
