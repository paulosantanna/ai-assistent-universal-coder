from __future__ import annotations

import json
from pathlib import Path
from aeos.core.evidence.evidence_store import EvidenceStore
from aeos.core.redaction.redactor import Redactor

from .workflow_models import DatasetCandidate, candidate_id


class TrainingDataCurator:
    def __init__(
        self,
        workspace_root: str = ".",
        evidence_store: EvidenceStore | None = None,
    ):
        self.workspace_root = Path(workspace_root).resolve()
        self.evidence_store = evidence_store or EvidenceStore()
        self.redactor = Redactor()

    def curate(
        self,
        *,
        execution_id: str,
        dataset_type: str,
        prompt: str,
        completion: str,
        source_refs: list[str],
        tests_passed: bool = False,
        judge_status: str | None = None,
        eval_score: float | None = None,
    ) -> DatasetCandidate:
        blocking: list[str] = []
        if not source_refs:
            blocking.append("source_refs_required")
        if dataset_type == "positive" and not tests_passed:
            blocking.append("positive_example_requires_passing_tests")
        if dataset_type == "positive" and judge_status in {"BLOCKED", "FAILED_VERIFICATION", "ERROR"}:
            blocking.append("judge_blocked_positive_example")
        if self._contains_forbidden_training_content(prompt) or self._contains_forbidden_training_content(completion):
            blocking.append("forbidden_training_content")

        redacted_prompt, prompt_findings = self.redactor.redact(prompt)
        redacted_completion, completion_findings = self.redactor.redact(completion)
        if prompt_findings or completion_findings:
            blocking.append("secret_or_sensitive_pattern_redacted")

        candidate = DatasetCandidate(
            candidate_id=candidate_id(),
            execution_id=execution_id,
            dataset_type=dataset_type,
            status="REJECTED" if blocking else "ACCEPTED",
            source_refs=source_refs,
            prompt=redacted_prompt,
            completion=redacted_completion,
            quality={
                "tests_passed": tests_passed,
                "judge_status": judge_status,
                "eval_score": eval_score,
            },
            redaction_findings=prompt_findings + completion_findings,
            blocking_conditions=blocking,
        )
        self._persist_candidate(candidate)
        self.evidence_store.store_record(execution_id, "dataset-candidate", candidate.to_dict())
        return candidate

    def _contains_forbidden_training_content(self, value: str) -> bool:
        lower = value.lower()
        forbidden_markers = (
            "chain_of_thought:",
            "chain-of-thought:",
            "<hidden_reasoning>",
            "<chain_of_thought>",
        )
        return any(marker in lower for marker in forbidden_markers)

    def _persist_candidate(self, candidate: DatasetCandidate) -> str:
        base = self.workspace_root / ".aeos" / "datasets" / candidate.dataset_type
        base.mkdir(parents=True, exist_ok=True)
        path = base / "dataset-candidates.jsonl"
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(candidate.to_dict(), ensure_ascii=False) + "\n")
        return str(path)

