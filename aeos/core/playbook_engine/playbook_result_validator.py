from __future__ import annotations

from typing import Any

from aeos.core.playbook_engine.playbook_models import PlaybookResult, PlaybookContract


class PlaybookResultValidator:
    def validate(self, result: PlaybookResult, contract: PlaybookContract) -> dict[str, Any]:
        findings: list[str] = []
        warnings: list[str] = []

        if result.status == "PASS" and result.blocking_conditions:
            findings.append("Status is PASS but blocking_conditions is not empty")

        if result.status == "PASS" and not result.facts and not result.recommendations:
            findings.append("PASS result has no facts or recommendations")

        if result.status == "PASS":
            for sr in result.skill_results:
                if sr.get("status") == "BLOCKED":
                    findings.append(f"Playbook returned PASS but skill '{sr.get('skill_id', '?')}' returned BLOCKED")

        if result.status not in ("PASS", "BLOCKED", "ERROR", "WAITING_APPROVAL"):
            findings.append(f"Invalid status: {result.status}")

        if not result.evidence_refs:
            warnings.append("No evidence_refs recorded")

        for fact in result.facts:
            claim = fact.get("claim", "")
            evidence = fact.get("evidence", "")
            if claim and not evidence:
                warnings.append(f"Fact '{claim[:50]}' has no evidence reference")

        return {
            "valid": len(findings) == 0,
            "findings": findings,
            "warnings": warnings,
        }
