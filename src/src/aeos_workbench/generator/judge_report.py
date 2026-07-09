"""Judge Report Generator - produces judge-report.md."""

from datetime import datetime, timezone


class JudgeReportGenerator:
    def __init__(self, judge_result, evidence_list):
        self.judge = judge_result
        self.evidence = evidence_list

    def generate(self):
        j = self.judge
        lines = []

        lines.append("# AEOS Judge Report\n")
        lines.append(f"**Judge:** {j.get('judge_id', 'unknown')}")
        lines.append(f"**Timestamp:** {j.get('timestamp', datetime.now(timezone.utc).isoformat())}")
        lines.append(f"**Evidence Count:** {j.get('evidence_count', 0)}")
        lines.append(f"**Version:** 1.0.0\n")

        # Decision Banner
        decision = j.get("decision", "UNKNOWN")
        if decision == "PASS":
            banner = "## ✅ PASS"
        elif decision == "NEEDS_REWORK":
            banner = "## ⚠️ NEEDS_REWORK"
        elif decision == "BLOCKED":
            banner = "## ⛔ BLOCKED"
        else:
            banner = f"## {decision}"
        lines.append(banner)
        lines.append("")

        lines.append(f"| Metric | Value |")
        lines.append(f"|--------|-------|")
        lines.append(f"| Final Score | **{j.get('final_score', 0)}/10** |")
        lines.append(f"| Deductions | {j.get('deductions', 0)} |")
        lines.append(f"| Decision | **{decision}** |")
        if j.get("blocking_reason"):
            lines.append(f"| Blocking Reason | {j['blocking_reason']} |")
        lines.append("")

        # Score Breakdown
        lines.append("## Score Breakdown\n")
        lines.append("| Category | Score | Weight | Weighted |")
        lines.append("|----------|-------|--------|----------|")
        for cat, info in [
            ("evidence_completeness", dict(weight=0.25, description="Evidence Completeness")),
            ("test_coverage", dict(weight=0.20, description="Test Coverage")),
            ("security_validation", dict(weight=0.20, description="Security Validation")),
            ("rollback_readiness", dict(weight=0.15, description="Rollback Readiness")),
            ("diff_quality", dict(weight=0.10, description="Diff Quality")),
            ("code_quality", dict(weight=0.10, description="Code Quality")),
        ]:
            score = j.get("scores", {}).get(cat, 0)
            weighted = round(score * info["weight"], 2)
            lines.append(f"| {info['description']} | {score} | {info['weight']} | {weighted} |")
        lines.append(f"| **Total** | | | **{j.get('final_score', 0)}** |")
        lines.append("")

        # Evidence Summary
        lines.append("## Evidence Reviewed\n")
        if self.evidence:
            lines.append("| ID | Type | Claim |")
            lines.append("|----|------|-------|")
            for ev in self.evidence[:20]:  # show top 20
                claim = ev["claim"][:70] + "..." if len(ev["claim"]) > 70 else ev["claim"]
                lines.append(f"| {ev.get('evidence_id', '?')} | {ev.get('type', '?')} | {claim} |")
            if len(self.evidence) > 20:
                lines.append(f"| ... | ... | ({len(self.evidence) - 20} more) |")
        else:
            lines.append("*No evidence submitted for review.*")
        lines.append("")

        # Failures
        failures = j.get("failures", [])
        if failures:
            lines.append("## Failures & Issues\n")
            for f in failures:
                lines.append(f"- ❌ {f}")
            lines.append("")

        # Blocking Conditions
        blocking = j.get("blocking_conditions", [])
        if blocking:
            lines.append("## Blocking Conditions\n")
            for bc in blocking:
                lines.append(f"- ⛔ `{bc}`")
            lines.append("")

        # Missing Evidence
        missing = j.get("missing_evidence_types", [])
        if missing:
            lines.append("## Missing Evidence Types\n")
            for m in missing:
                lines.append(f"- `{m}`")
            lines.append("")

        # Next Steps
        next_steps = j.get("next_steps", [])
        if next_steps:
            lines.append("## Next Steps\n")
            for i, step in enumerate(next_steps, 1):
                lines.append(f"{i}. {step}")
            lines.append("")

        lines.append("---\n")
        lines.append(f"*AEOS Judge Report v1.0.0 — Decision: {decision} — Score: {j.get('final_score', 0)}/10*")

        return "\n".join(lines)
