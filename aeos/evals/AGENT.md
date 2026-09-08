# AEOS Evals contract

Governance: CodENavi Full Workspace v2

Inherits root `AGENT.md` and `references/CODENAVI_FULL_WORKSPACE_STANDARD.md`.

All evals follow **BRIEFING → RECON → PLAN → EXECUTE → VERIFY → DEBRIEF**.

Every eval must define:
- behavior/capability being measured;
- dataset/corpus provenance and contamination risk;
- baseline and acceptance threshold;
- reproducibility controls where possible;
- failure semantics and regression interpretation;
- separate retrieval/generation/tool measurements when applicable;
- no tuning exclusively to the benchmark;
- evidence artifacts sufficient to reproduce the conclusion.

AI/model/provider evals are freshness-sensitive. Model labels alone are not conclusions; compare candidates under the same harness and constraints.
