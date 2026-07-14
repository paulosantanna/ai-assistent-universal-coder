from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class ActionFailure(BaseModel):
    failure_id: str
    workflow_run_id: str
    job_id: str
    step_name: str
    category: str
    fingerprint: str
    summary: str
    root_cause_hypothesis: str
    confidence: float
    assigned_subagent: str
    evidence_refs: List[str]
    retryable: bool
    code_change_required: bool
    human_action_required: bool
