from __future__ import annotations

from typing import Any

from aeos.core.judge.judge_models import BlockingRule

BLOCKING_RULES_REGISTRY: dict[str, BlockingRule] = {
    "missing_evidence_manifest": BlockingRule(
        rule_id="missing_evidence_manifest",
        severity="critical",
        category="evidence_integrity",
        description="Evidence manifest is missing",
    ),
    "manifest_hash_mismatch": BlockingRule(
        rule_id="manifest_hash_mismatch",
        severity="critical",
        category="evidence_integrity",
        description="Evidence manifest SHA256 hash does not match computed hash",
    ),
    "permission_denied": BlockingRule(
        rule_id="permission_denied",
        severity="critical",
        category="permissions",
        description="Permission was denied for a requested action",
    ),
    "policy_denied": BlockingRule(
        rule_id="policy_denied",
        severity="critical",
        category="policy",
        description="Policy engine denied an action",
    ),
    "governance_blocked": BlockingRule(
        rule_id="governance_blocked",
        severity="critical",
        category="governance",
        description="Governance gate blocked the execution",
    ),
    "tool_router_bypass": BlockingRule(
        rule_id="tool_router_bypass",
        severity="critical",
        category="security",
        description="Tool router was bypassed or not called",
    ),
    "direct_mcp_call": BlockingRule(
        rule_id="direct_mcp_call",
        severity="critical",
        category="security",
        description="Direct MCP call detected without going through tool router",
    ),
    "direct_shell_call": BlockingRule(
        rule_id="direct_shell_call",
        severity="critical",
        category="security",
        description="Direct shell call detected without going through tool router",
    ),
    "secret_exposed": BlockingRule(
        rule_id="secret_exposed",
        severity="critical",
        category="security",
        description="Secret or API key was exposed in output",
    ),
    "raw_secret_persisted": BlockingRule(
        rule_id="raw_secret_persisted",
        severity="critical",
        category="security",
        description="Raw secret was persisted to disk",
    ),
    "write_outside_allowed_scope": BlockingRule(
        rule_id="write_outside_allowed_scope",
        severity="critical",
        category="filesystem",
        description="Write operation detected outside allowed scope",
    ),
    "package_verify_failed": BlockingRule(
        rule_id="package_verify_failed",
        severity="critical",
        category="supply_chain",
        description="Package verification failed",
    ),
    "path_traversal_detected": BlockingRule(
        rule_id="path_traversal_detected",
        severity="critical",
        category="security",
        description="Path traversal attack detected",
    ),
    "approval_missing": BlockingRule(
        rule_id="approval_missing",
        severity="critical",
        category="approval",
        description="Required approval is missing",
    ),
    "approval_expired": BlockingRule(
        rule_id="approval_expired",
        severity="critical",
        category="approval",
        description="Approval has expired",
    ),
    "approval_wildcard": BlockingRule(
        rule_id="approval_wildcard",
        severity="critical",
        category="approval",
        description="Wildcard approval detected (not allowed)",
    ),
    "auto_merge_detected": BlockingRule(
        rule_id="auto_merge_detected",
        severity="critical",
        category="git",
        description="Auto-merge operation detected",
    ),
    "auto_deploy_detected": BlockingRule(
        rule_id="auto_deploy_detected",
        severity="critical",
        category="deployment",
        description="Auto-deploy operation detected",
    ),
    "force_push_detected": BlockingRule(
        rule_id="force_push_detected",
        severity="critical",
        category="git",
        description="Force push to protected branch detected",
    ),
    "protected_branch_mutation": BlockingRule(
        rule_id="protected_branch_mutation",
        severity="critical",
        category="git",
        description="Mutation on protected branch detected",
    ),
    "critical_mcp_enabled_by_default": BlockingRule(
        rule_id="critical_mcp_enabled_by_default",
        severity="critical",
        category="mcp",
        description="Critical MCP tool was enabled by default",
    ),
    "unsupported_claim": BlockingRule(
        rule_id="unsupported_claim",
        severity="high",
        category="integrity",
        description="Claim without supporting evidence",
    ),
    "skill_blocked": BlockingRule(
        rule_id="skill_blocked",
        severity="high",
        category="skill_engine",
        description="Skill execution was blocked",
    ),
    "playbook_blocked": BlockingRule(
        rule_id="playbook_blocked",
        severity="high",
        category="playbook_engine",
        description="Playbook execution was blocked",
    ),
    "agent_blocked": BlockingRule(
        rule_id="agent_blocked",
        severity="high",
        category="agent_runtime",
        description="Agent task was blocked",
    ),
    "runtime_error": BlockingRule(
        rule_id="runtime_error",
        severity="critical",
        category="runtime",
        description="Runtime error occurred during execution",
    ),
    "tests_failed": BlockingRule(
        rule_id="tests_failed",
        severity="high",
        category="quality",
        description="Tests failed during execution",
    ),
    "smoke_test_failed": BlockingRule(
        rule_id="smoke_test_failed",
        severity="high",
        category="quality",
        description="Smoke tests failed",
    ),
    "performance_budget_unreported": BlockingRule(
        rule_id="performance_budget_unreported",
        severity="medium",
        category="performance",
        description="Performance budget not reported",
    ),
    "performance_budget_breached_without_justification": BlockingRule(
        rule_id="performance_budget_breached_without_justification",
        severity="high",
        category="performance",
        description="Performance budget breached without justification",
    ),
}

CRITICAL_RULES = {
    rid for rid, rule in BLOCKING_RULES_REGISTRY.items()
    if rule.severity == "critical"
}

HIGH_RULES = {
    rid for rid, rule in BLOCKING_RULES_REGISTRY.items()
    if rule.severity == "high"
}


def get_rule(rule_id: str) -> BlockingRule:
    return BLOCKING_RULES_REGISTRY.get(rule_id)


def is_critical(rule_id: str) -> bool:
    rule = get_rule(rule_id)
    return rule is not None and rule.severity == "critical"


def get_severity(rule_id: str) -> str:
    rule = get_rule(rule_id)
    return rule.severity if rule else "unknown"


def get_category(rule_id: str) -> str:
    rule = get_rule(rule_id)
    return rule.category if rule else "unknown"
