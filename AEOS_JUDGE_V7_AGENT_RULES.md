# AEOS Judge v7 — Agent Runtime Rules

Judge v7 must block when:

- agent executed a tool directly;
- agent bypassed Tool Router;
- agent exceeded delegated scope;
- subagent delegated without permission;
- implementing agent judged its own work;
- context includes raw secret;
- memory write lacks evidence;
- task graph has unresolved required task;
- high-risk task lacks Security Agent review;
- code-related task lacks rollback plan;
- task output has unsupported facts;
- agent trace is missing;
- conflicting agent outputs are unresolved;
- approval-required task executed without approval.

Judge v7 may PASS only when:

- task graph completed or blocked explicitly;
- all required agents produced outputs;
- all required evidence exists;
- all agent traces exist;
- all policies passed;
- all permission decisions exist;
- no agent exceeded authority;
- final report distinguishes facts, assumptions, risks, and recommendations.
