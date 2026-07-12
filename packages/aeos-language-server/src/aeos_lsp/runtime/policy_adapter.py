from __future__ import annotations

import logging
from typing import Any

from aeos_lsp.runtime.ports import PolicyDecision, PolicyPort

logger = logging.getLogger(__name__)


class PolicyAdapter(PolicyPort):
    def __init__(self) -> None:
        self._initialized = False
        self._policies: dict[str, dict[str, Any]] = {}

    async def initialize(self, config: dict[str, Any] | None = None) -> None:
        self._initialized = True
        if config and "policies" in config:
            self._policies.update(config["policies"])
        logger.info("Policy adapter initialized with %d policies", len(self._policies))

    async def shutdown(self) -> None:
        self._initialized = False
        self._policies.clear()
        logger.info("Policy adapter shut down")

    async def evaluate(
        self,
        action: str,
        resource: str,
        context: dict[str, Any],
    ) -> PolicyDecision:
        if not self._initialized:
            return PolicyDecision(compliant=False, policy_name="__uninitialized__", violations=["Adapter not initialized"])

        violations: list[str] = []
        matched_policy = ""

        for policy_name, policy_def in self._policies.items():
            rules = policy_def.get("rules", []) if isinstance(policy_def, dict) else []
            applicable = False
            for rule in rules:
                if isinstance(rule, dict):
                    if self._rule_matches(rule, action, resource, context):
                        applicable = True
                        if not self._rule_allows(rule, context):
                            violations.append(f"Policy '{policy_name}': {rule.get('deny_reason', rule.get('message', 'denied'))}")
                            if matched_policy == "":
                                matched_policy = policy_name

            if not applicable and policy_def.get("default", "allow") == "deny":
                violations.append(f"Policy '{policy_name}': no matching allow rule (default deny)")

        if not violations:
            return PolicyDecision(compliant=True)
        return PolicyDecision(
            compliant=False,
            policy_name=matched_policy or "unknown",
            violations=violations,
            remediation="Review policy rules and ensure action complies with all applicable policies.",
        )

    async def list_policies(self) -> list[dict[str, Any]]:
        return [
            {"name": name, **defn}
            for name, defn in self._policies.items()
        ]

    async def get_policy(self, policy_name: str) -> dict[str, Any] | None:
        return self._policies.get(policy_name)

    def add_policy(self, name: str, definition: dict[str, Any]) -> None:
        self._policies[name] = definition
        logger.info("Added policy: %s", name)

    def _rule_matches(self, rule: dict[str, Any], action: str, resource: str, context: dict[str, Any]) -> bool:
        rule_action = rule.get("action", "")
        rule_resource = rule.get("resource", "")
        if rule_action and rule_action not in action:
            return False
        if rule_resource and rule_resource not in resource:
            return False
        return True

    def _rule_allows(self, rule: dict[str, Any], context: dict[str, Any]) -> bool:
        effect = rule.get("effect", "deny")
        if effect == "allow":
            conditions = rule.get("conditions", {})
            if conditions:
                for key, expected in conditions.items():
                    actual = context.get(key)
                    if actual != expected:
                        return False
            return True
        return False

    async def health_check(self) -> dict[str, Any]:
        return {
            "status": "ok" if self._initialized else "not_initialized",
            "policy_count": len(self._policies),
        }
