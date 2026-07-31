from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from aeos.core.evidence.evidence_store import EvidenceStore

from .workflow_models import ModelRoutingDecision


class ModelRouter:
    def __init__(
        self,
        workspace_root: str = ".",
        aeos_root: str | None = None,
        evidence_store: EvidenceStore | None = None,
    ):
        self.workspace_root = Path(workspace_root).resolve()
        self.aeos_root = Path(aeos_root).resolve() if aeos_root else self.workspace_root
        self.evidence_store = evidence_store or EvidenceStore()
        self.config = self._load_config()

    def decide(
        self,
        *,
        execution_id: str,
        stage: str,
        risk_level: str,
        estimated_input_tokens: int,
        estimated_output_tokens: int = 2000,
        approval_id: str | None = None,
        deterministic_available: bool = False,
    ) -> ModelRoutingDecision:
        profiles = self.config["profiles"]
        profile_name = self._select_profile(stage, risk_level, deterministic_available)
        if risk_level == "low" and profiles[profile_name].get("paid", False) and approval_id is None:
            profile_name = "free_cloud" if stage in {"independent_review", "small_context_review"} else "free_local"
        profile = profiles[profile_name]
        paid = bool(profile.get("paid", False))
        total_tokens = estimated_input_tokens + estimated_output_tokens
        blocking: list[str] = []
        status = "PASS"

        if paid and self.config["approval"].get("require_for_paid_profiles", True) and not approval_id:
            status = "WAITING_APPROVAL"
            blocking.append("paid_model_requires_approval")
        if total_tokens > int(profile.get("max_context_tokens", 0)):
            status = "BLOCKED"
            blocking.append("context_exceeds_selected_profile")
        if deterministic_available and paid and self.config["blocking"].get("block_paid_when_deterministic_stage", True):
            status = "BLOCKED"
            blocking.append("deterministic_stage_must_not_use_paid_model")

        decision = ModelRoutingDecision(
            execution_id=execution_id,
            stage=stage,
            risk_level=risk_level,
            profile=profile_name,
            status=status,
            paid=paid,
            reason=self._reason(stage, risk_level, profile_name, deterministic_available),
            estimated_input_tokens=estimated_input_tokens,
            estimated_output_tokens=estimated_output_tokens,
            max_context_tokens=int(profile.get("max_context_tokens", 0)),
            approval_id=approval_id,
            blocking_conditions=blocking,
        )
        self._persist_decision(decision)
        self.evidence_store.store_record(execution_id, "model-routing-decision", decision.to_dict())
        return decision

    def _select_profile(self, stage: str, risk_level: str, deterministic_available: bool) -> str:
        if deterministic_available or stage in self.config["profiles"]["deterministic"].get("stages", []):
            return "deterministic"
        for profile_name, profile in self.config["profiles"].items():
            if stage in profile.get("stages", []) and profile_name != "deterministic":
                return profile_name
        return self.config["escalation"].get(risk_level, self.config.get("default_profile", "free_local"))

    def _reason(self, stage: str, risk_level: str, profile_name: str, deterministic_available: bool) -> str:
        if deterministic_available:
            return "deterministic_tooling_available"
        return f"stage={stage};risk={risk_level};profile={profile_name}"

    def _load_config(self) -> dict[str, Any]:
        path = self.aeos_root / "aeos" / "config" / "model-router.config.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return data["model_router"]

    def _persist_decision(self, decision: ModelRoutingDecision) -> str:
        base = self.workspace_root / ".aeos" / "evidence" / decision.execution_id
        base.mkdir(parents=True, exist_ok=True)
        path = base / "model-routing-decisions.jsonl"
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(decision.to_dict(), ensure_ascii=False) + "\n")
        return str(path)

