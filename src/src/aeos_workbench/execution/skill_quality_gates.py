"""Skill Quality Gates — validates skill execution against contract rules."""

from pathlib import Path


class SkillQualityGates:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def validate(self, skill_definition: dict, execution_context: dict) -> dict:
        self.errors = []
        self.warnings = []

        allowed = skill_definition.get("allowed_actions", skill_definition.get("allowed", []))
        forbidden = skill_definition.get("forbidden_actions", skill_definition.get("forbidden", []))
        gates = skill_definition.get("quality_gates", [])
        required_evidence = skill_definition.get("required_evidence", skill_definition.get("evidence_required", []))

        performed_actions = execution_context.get("performed_actions", [])

        self._check_allowed_actions(performed_actions, allowed)
        self._check_forbidden_actions(performed_actions, forbidden)
        self._check_quality_gates(gates, execution_context)
        self._check_required_evidence(required_evidence, execution_context)

        return {
            "passed": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
            "gate_count": len(gates),
            "evidence_required": len(required_evidence),
        }

    def _check_allowed_actions(self, performed: list[str], allowed: list[str]):
        for action in performed:
            if action not in allowed:
                self.errors.append(f"Action '{action}' is not in allowed list")

    def _check_forbidden_actions(self, performed: list[str], forbidden: list[str]):
        for action in performed:
            if action in forbidden:
                self.errors.append(f"Forbidden action '{action}' was performed")

    def _check_quality_gates(self, gates: list[str], ctx: dict):
        for gate in gates:
            gate_lower = gate.lower()
            if "must reflect actual code" in gate_lower or "must cite" in gate_lower:
                if not ctx.get("has_file_citations"):
                    self.errors.append(f"Quality gate failed: {gate}")
            if "must cover all public" in gate_lower:
                if not ctx.get("public_apis_covered"):
                    self.errors.append(f"Quality gate failed: {gate}")
            if "must include at least one diagram" in gate_lower:
                if not ctx.get("has_diagram"):
                    self.warnings.append(f"Quality gate warning: {gate}")
            if "must pass documentation standards" in gate_lower or "must pass" in gate_lower:
                if not ctx.get("standards_validated"):
                    self.errors.append(f"Quality gate failed: {gate}")
            if "must distinguish" in gate_lower:
                if not ctx.get("facts_distinguished_from_assumptions"):
                    self.warnings.append(f"Quality gate warning: {gate}")
            if "must flag inconsistent" in gate_lower:
                if not ctx.get("inconsistencies_flagged"):
                    self.warnings.append(f"Quality gate warning: {gate}")

    def _check_required_evidence(self, required: list[str], ctx: dict):
        collected = ctx.get("collected_evidence", [])
        for req in required:
            if req not in collected:
                self.warnings.append(f"Required evidence '{req}' not collected")