from __future__ import annotations

import json
from typing import Any


class PromptOptimizer:
    """Build bounded AEOS prompts with evidence and stop-condition discipline."""

    def optimize(
        self,
        goal: str,
        constraints: list[str],
        output_schema: dict[str, Any],
        required_inputs: list[str] | None = None,
        evidence_refs: list[str] | None = None,
        token_budget: str | None = None,
    ) -> str:
        required_inputs = required_inputs or ["objective", "target", "constraints", "evidence_refs"]
        evidence_refs = evidence_refs or []
        token_budget = token_budget or "bounded by active AEOS profile"

        return f"""
Objective:
{goal.strip()}

Scope and boundaries:
- Execute only the requested task.
- Treat missing context as an explicit assumption or blocker.
- Do not expand scope, mutate state or call tools outside the declared permissions.

Required inputs:
{self._bullets(required_inputs)}

Evidence rules:
- Use evidence-backed facts only.
- Mark assumptions explicitly.
- Reference inspected files, command results, generated artifacts or registry entries.
- Current evidence refs: {self._inline_list(evidence_refs)}

Constraints:
{self._bullets(constraints)}

Tool and permission boundaries:
- Route tool access through Tool Router, MCP runtime or the approved command layer.
- Respect Permission Engine, Policy Engine, approval gates and sandbox limits.
- Redact secrets, tokens, cookies, credentials and sensitive values.

Output schema:
```json
{json.dumps(output_schema, indent=2, sort_keys=True)}
```

Quality gates:
- Facts cite evidence.
- Risks include severity or impact.
- Recommendations include action and rationale.
- Output follows the declared schema.
- Token budget: {token_budget}.

Stop conditions:
- required input or evidence is missing;
- permission, policy or approval is denied;
- required tool access is unavailable;
- secret or sensitive value would appear in output;
- tool access is not routed through Tool Router or MCP runtime;
- validation cannot be completed.
""".strip()

    @staticmethod
    def _bullets(items: list[str]) -> str:
        if not items:
            return "- none"
        return "\n".join(f"- {item}" for item in items)

    @staticmethod
    def _inline_list(items: list[str]) -> str:
        if not items:
            return "none provided"
        return ", ".join(items)
