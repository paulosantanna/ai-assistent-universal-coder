---
name: laya-expert
description: "Implement calibrated typed decisions with the Laya SDK. Use for Laya decisions or RLCD training. Do NOT use for open-ended text or GraphRAG."
license: CC-BY-4.0
metadata:
  author: AEOS
  version: 0.1.0
  owner_agent: codenavi-agent
---

# laya-expert

Governance: CodENavi Full Workspace v2 (BRIEFING→DEBRIEF); skill of `codenavi-agent`; inherits `AGENTS.md`. Lenses are internal; no new agent identities; no bypass of secret or permission gates.

## Outcome
Implement, fine-tune and evaluate bounded Laya decisions with calibrated uncertainty.

## Workflow
1. Inspect official release, installed SDK and checkpoint schema/revision; distinguish Laya from LoRA and from a generative LLM.
2. Define bounded choice/score/noul questions, expected typed labels, token budgets, baseline and explicit confidence fallback.
3. Run actual inference with the official SDK; evaluate label accuracy, calibration and option-order sensitivity before granting decision influence.
4. Prepare source-family-disjoint train/validation/test data; reserve human review and verify JSONL typed labels against installed training APIs.
5. Train RLCD with a bounded GPU budget, held-out calibration and exact base/dataset/package identities; save a reloadable compatible checkpoint.
6. Compare base/tuned decisions and ECE on frozen data; record uncertainty and keep execution authorization in deterministic code.

## Inputs, outputs and stop
Inputs: authorized corpus/project, source identities, actual runtime capabilities and frozen evaluation goal.
Outputs: source-backed artifacts, relevant runtime behavior/checkpoints and reproducible verification evidence.
Missing source/license/runtime/permission blocks the dependent step; continue independent authorized work.
Never persist credentials, claim unrun checks passed or create another agent identity.

## Modules — progressive disclosure
- Read [intake and gates](references/intake.md) before a material mission or choosing providers.
- Read [technical procedure](references/procedure.md) for implementation, analysis or troubleshooting.
- Read [runtime integration](references/runtime.md) when invoking the MCP, API or live graph.
- Read [evaluation](references/evaluation.md) before accepting quality or training results.
- Read [examples and failures](references/examples.md) for concrete invocation or a failed prerequisite.
- Read [sources and attribution](references/sources.md) when verifying facts, APIs or upstream versions.

## Response

Output: result first, then evidence (paths, commands, results), blockers and next step. No narration or restated instructions. Follow a defined output schema exactly. Reply in the user's language.
