from __future__ import annotations

import logging
from typing import Any

from aeos_lsp.runtime.ports import JudgePort, JudgeVerdict

logger = logging.getLogger(__name__)


class JudgeAdapter(JudgePort):
    def __init__(self) -> None:
        self._initialized = False
        self._rules: list[dict[str, Any]] = []

    async def initialize(self, config: dict[str, Any] | None = None) -> None:
        self._initialized = True
        if config and "rules" in config:
            self._rules = list(config["rules"])
        logger.info("Judge adapter initialized with %d rules", len(self._rules))

    async def shutdown(self) -> None:
        self._initialized = False
        self._rules.clear()
        logger.info("Judge adapter shut down")

    async def evaluate(
        self,
        artifact: str,
        rules: list[dict[str, Any]] | None = None,
        context: dict[str, Any] | None = None,
    ) -> JudgeVerdict:
        if not self._initialized:
            return JudgeVerdict(passed=False, score=0.0, summary="Judge adapter not initialized")

        active_rules = rules if rules is not None else self._rules
        if not active_rules:
            return JudgeVerdict(passed=True, score=1.0, summary="No rules to evaluate")

        check_results: list[dict[str, Any]] = []
        passed_count = 0

        for rule in active_rules:
            rule_name = rule.get("name", "unnamed")
            rule_type = rule.get("type", "contains")
            rule_value = rule.get("value", "")
            rule_weight = float(rule.get("weight", 1.0))

            passed = self._check_rule(rule_type, rule_value, artifact, context or {})

            check_results.append({
                "rule": rule_name,
                "type": rule_type,
                "passed": passed,
                "weight": rule_weight,
            })

            if passed:
                passed_count += 1

        total_weight = sum(r.get("weight", 1.0) for r in check_results)
        passed_weight = sum(r.get("weight", 1.0) for r in check_results if r["passed"])
        score = passed_weight / total_weight if total_weight > 0 else 1.0

        return JudgeVerdict(
            passed=passed_count == len(check_results),
            score=score,
            checks=check_results,
            summary=f"Passed {passed_count}/{len(check_results)} checks (score: {score:.2f})",
        )

    async def get_rules(self) -> list[dict[str, Any]]:
        return list(self._rules)

    def add_rule(self, rule: dict[str, Any]) -> None:
        self._rules.append(rule)
        logger.info("Added judge rule: %s", rule.get("name", "unnamed"))

    def _check_rule(
        self,
        rule_type: str,
        rule_value: str,
        artifact: str,
        context: dict[str, Any],
    ) -> bool:
        if rule_type == "contains":
            return rule_value.lower() in artifact.lower()
        elif rule_type == "not_contains":
            return rule_value.lower() not in artifact.lower()
        elif rule_type == "min_length":
            try:
                return len(artifact) >= int(rule_value)
            except (ValueError, TypeError):
                return False
        elif rule_type == "max_length":
            try:
                return len(artifact) <= int(rule_value)
            except (ValueError, TypeError):
                return False
        elif rule_type == "regex":
            import re
            try:
                return bool(re.search(rule_value, artifact))
            except re.error:
                return False
        elif rule_type == "starts_with":
            return artifact.startswith(rule_value)
        elif rule_type == "ends_with":
            return artifact.endswith(rule_value)
        elif rule_type == "context_match":
            expected = context.get(rule_value)
            return expected is not None and str(expected).lower() in artifact.lower()
        else:
            logger.warning("Unknown judge rule type: %s", rule_type)
            return True

    async def health_check(self) -> dict[str, Any]:
        return {
            "status": "ok" if self._initialized else "not_initialized",
            "rule_count": len(self._rules),
        }
