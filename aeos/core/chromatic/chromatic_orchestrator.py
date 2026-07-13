from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


COLOR_RULES: dict[str, list[str]] = {
    "WHITE": ["evidence", "unknown", "uncertain", "fact", "source", "verify", "research"],
    "BLUE": ["architecture", "system", "dependency", "design", "migration", "scale", "cloud"],
    "RED": ["security", "risk", "failure", "bug", "attack", "threat", "regression"],
    "GREEN": ["implement", "delivery", "code", "test", "deploy", "plan", "fix"],
    "YELLOW": ["optimize", "performance", "opportunity", "cost", "reuse", "improve", "evolve"],
    "PURPLE": ["knowledge", "memory", "lesson", "learn", "standard", "history", "context"],
    "ORANGE": ["user", "product", "team", "workflow", "adoption", "operation", "ux"],
    "BLACK": ["constraint", "approval", "regulatory", "legal", "prohibited", "secret", "policy"],
}


DEFAULT_PAIRS: dict[str, list[str]] = {
    "architecture": ["WHITE", "BLUE", "RED", "GREEN"],
    "security": ["WHITE", "RED", "BLACK", "GREEN"],
    "performance": ["WHITE", "BLUE", "YELLOW", "GREEN"],
    "strategy": ["WHITE", "BLUE", "RED", "YELLOW", "ORANGE"],
    "learning": ["WHITE", "PURPLE", "RED", "BLUE"],
    "cloud": ["WHITE", "BLUE", "RED", "GREEN", "BLACK"],
    "evolution": ["WHITE", "BLUE", "YELLOW", "GREEN", "PURPLE"],
    "migration": ["WHITE", "BLUE", "RED", "GREEN", "BLACK"],
}


COLOR_PURPOSES: dict[str, str] = {
    "WHITE": "Evidence, facts, uncertainty and source quality.",
    "BLUE": "Architecture, boundaries, dependencies and long-term system coherence.",
    "RED": "Risk, adversarial review, security and credible failure modes.",
    "GREEN": "Implementation path, test strategy and delivery sequencing.",
    "YELLOW": "Opportunity, leverage, optimization and reuse.",
    "PURPLE": "Prior knowledge, memory, standards and reusable lessons.",
    "ORANGE": "Human, product, workflow and operational fit.",
    "BLACK": "Constraints, policy, stop conditions and approval boundaries.",
}


@dataclass(frozen=True)
class ChromaticRun:
    run_id: str
    objective: str
    selected_colors: list[str]
    decision_type: str
    handoffs: list[dict[str, Any]] = field(default_factory=list)
    decision_matrix: list[dict[str, Any]] = field(default_factory=list)
    quality_gates: list[str] = field(default_factory=list)
    blocking_conditions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "objective": self.objective,
            "selected_colors": self.selected_colors,
            "decision_type": self.decision_type,
            "handoffs": self.handoffs,
            "decision_matrix": self.decision_matrix,
            "quality_gates": self.quality_gates,
            "blocking_conditions": self.blocking_conditions,
        }


class ChromaticOrchestrator:
    """Small deterministic adapter for using Chromatic Mega Brain inside AEOS runtime."""

    def select_colors(self, objective: str, decision_type: str = "architecture", max_colors: int = 5) -> list[str]:
        lower = f"{objective} {decision_type}".lower()
        scores = {color: 0 for color in COLOR_RULES}
        for color, terms in COLOR_RULES.items():
            scores[color] = sum(1 for term in terms if term in lower)

        for topic, colors in DEFAULT_PAIRS.items():
            if topic in lower:
                for color in colors:
                    scores[color] += 2

        selected = [color for color, score in sorted(scores.items(), key=lambda item: (-item[1], item[0])) if score > 0]
        if "WHITE" not in selected:
            selected.insert(0, "WHITE")
        if len(selected) < 2:
            selected.append("BLUE")
        return selected[: max(2, min(max_colors, 8))]

    def create_run(
        self,
        objective: str,
        decision_type: str = "architecture",
        constraints: list[str] | None = None,
        evidence_refs: list[str] | None = None,
        max_colors: int = 5,
    ) -> ChromaticRun:
        selected_colors = self.select_colors(objective, decision_type, max_colors=max_colors)
        constraints = constraints or []
        evidence_refs = evidence_refs or []
        blocking_conditions = []
        if not objective.strip():
            blocking_conditions.append("objective is required")
        if decision_type in ("cloud-readiness", "architecture", "migration") and not evidence_refs:
            blocking_conditions.append("evidence_refs required for high-impact chromatic decisions")

        return ChromaticRun(
            run_id=f"cbrain-{uuid4().hex[:12]}",
            objective=objective,
            selected_colors=selected_colors,
            decision_type=decision_type,
            handoffs=[
                self._handoff(color, objective, constraints, evidence_refs)
                for color in selected_colors
            ],
            decision_matrix=self._decision_matrix(decision_type),
            quality_gates=[
                "Use the smallest useful color set.",
                "Separate evidence, inference and assumptions.",
                "Expose contradictions before recommendation.",
                "Route final recommendation through Judge for high-impact changes.",
                "Promote lessons only after validation evidence exists.",
            ],
            blocking_conditions=blocking_conditions,
        )

    def _handoff(
        self,
        color: str,
        objective: str,
        constraints: list[str],
        evidence_refs: list[str],
    ) -> dict[str, Any]:
        return {
            "color": color,
            "purpose": COLOR_PURPOSES[color],
            "objective": f"Analyze the objective from the {color} perspective.",
            "problem_frame": objective,
            "scope": "Assigned color contract only",
            "excluded_scope": "Final integrated decision",
            "constraints": constraints,
            "evidence_refs": evidence_refs,
            "expected_output": "facts, assumptions, risks, recommendation and unresolved questions",
            "stop_conditions": [
                "insufficient evidence",
                "policy or permission conflict",
                "claim would require unsupported inference",
            ],
        }

    def _decision_matrix(self, decision_type: str) -> list[dict[str, Any]]:
        base = [
            {"criterion": "Evidence strength", "owner_color": "WHITE", "weight": 3},
            {"criterion": "Architecture fit", "owner_color": "BLUE", "weight": 3},
            {"criterion": "Risk and reversibility", "owner_color": "RED", "weight": 3},
            {"criterion": "Implementation cost", "owner_color": "GREEN", "weight": 2},
            {"criterion": "Operational fit", "owner_color": "ORANGE", "weight": 2},
        ]
        if decision_type in ("cloud-readiness", "migration", "security"):
            base.append({"criterion": "Policy and stop conditions", "owner_color": "BLACK", "weight": 3})
        if decision_type in ("evolution", "strategy", "performance"):
            base.append({"criterion": "Leverage and reusable learning", "owner_color": "YELLOW", "weight": 2})
        return base
