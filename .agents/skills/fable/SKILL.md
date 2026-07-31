---
name: fable
description: Standard problem-solving loop (classify ask, define done, gather evidence, decide, act surgically, verify by observation, report outcome-first). Use for non-trivial multi-step tasks, diagnosis, planning, or auditing work.
---

# Enterprise Skill: fable

## Mission

Provide enterprise-grade Fable Method problem-solving loop capability inside AEOS v1.1.

## Production Scope

This skill governs multi-step problem solving across coding, devops, research, data analysis, business operations, finance, legal compliance, and design/UX. It enforces evidence-backed decisions, surgical execution, double-verification, and outcome-first reporting.

## Allowed Actions

- Read authorized workspace files, specs, and configurations through Tool Router.
- Perform bounded parallel research (web, documentation, source code).
- Execute local non-destructive verification commands (tests, builds, lints, dry-runs).
- Generate reports, plans, audit summaries, and candidate lessons.
- Route domain-specific tasks to domain adapters (`references/domains/`).

## Forbidden Actions

- Direct un-routed tool execution or filesystem bypass.
- Secret, key, or credential reading/exposure.
- Unauthorized outward or irreversible actions (commits, pushes, deploys, deletes, payments) without explicit user authorization quotes.
- Verification theater (claiming tests passed without running them or inspecting output).
- Silent step-dropping or scope expansion beyond declared boundaries.
- Fabricating data, API signatures, endpoints, or evidence from memory.

## Required Inputs

```yaml
input:
  task_or_ask: "The core problem, question, or change request"
  mode: "full (default) | plan | audit | report"
  domain: "coding (default) | devops | research | data-analysis | business-ops | finance | legal-compliance | design-ux | marketing"
  evidence_refs: []
```

## Required Output Schema

```json
{
  "skill_id": "fable",
  "status": "PASS|BLOCKED|REVIEW",
  "shape": "task|assessment|plan-first",
  "facts": [],
  "assumptions": [],
  "risks": [],
  "recommendations": [],
  "evidence_refs": [],
  "verifications": {
    "done_criterion": "",
    "surrounding_system_healthy": true,
    "twins_searched": ""
  },
  "gates": {
    "intent_line": "",
    "auth_line": "",
    "pending_line": "",
    "twins_line": ""
  },
  "blocking_conditions": []
}
```

## Prompt Contract

- State the objective, target scope, assumptions, and constraints before execution.
- Classify the ask shape (Question/Assessment, Task, Plan-first) before taking any action.
- Enforce the Triviality Gate and Fit Gate.
- Gather primary sources before modifying any behavior.
- Execute smallest correct changes with Intent Gate verification.
- Verify both target criteria and surrounding system health by direct observation.
- Report outcome-first with zero step headers or method scaffolding.

## Quality Gates

- Facts cite concrete evidence (`file:line`, command output, or fetched URL).
- Assumptions are explicit and checkable.
- Risks are classified with severity.
- Intent line (`INTENT:`) present whenever code/behavior changed.
- Auth line (`AUTH:`) present whenever outward/irreversible action was taken.
- Twins line (`TWINS:`) present whenever a defect fix was applied.
- Pending line (`PENDING:`) present when documented follow-up was deferred.

## Stop Conditions

- 3 consecutive failed fix-verify cycles on the same issue.
- Missing required human authorization for outward/irreversible actions.
- Unreachable primary evidence when inference alone is unsafe.
- Secret/credential exposure detected.

---

# The Fable Method Loop

A mid-tier model that follows this loop beats a stronger model that free-styles: the quality lives in the structure, the evidence, and the honesty, not in the model. The loop is self-contained. Follow it literally. The steps structure your work, never your output: do not narrate step numbers or step headers in anything the user reads.

## Usage

```
/fable <task>       full loop on the task (default)
/fable plan <task>  Steps 0-3 only: classify, define done, gather evidence, deliver the plan, stop
/fable audit        grade the work already done in this conversation against the loop
/fable report       rewrite the answer you were about to send per Step 6
```

Deeper material loads on demand:
- `references/failure-modes.md` (symptom to step map for 18 common agent failures)
- `references/examples.md` (full worked examples for every ask shape)
- `references/domains/` (domain adapters for devops, research, data analysis, business ops, finance, legal, design/UX, marketing)
- `references/flowcharts.md` (the whole method as decision flowcharts)

### Triviality Gate (run first)

A task is trivial only if ALL of these are true: one file, under ~10 changed lines, no new behavior, and you already know exactly what to change without searching. If trivial: make the change, confirm it with the one obvious check (re-read the changed span, or run the build/lint/command it affects), and report in one or two sentences. Everything else, and anything you are unsure about, gets the full loop.

### Fit Gate (run next, before Step 0)

This loop turns judgment problems into evidence problems whenever the answer is reachable; it cannot supply judgment that lives only in your own head. So first locate where the answer is, and route:

- **In sources you can open** (a spec, file, dataset, check, or docs): run the loop. This is the default.
- **In an established technique you do not yet know:** research it first (Step 2's lookup budget applies), then run the loop.
- **Only in your own inference, nothing to open or look up:** say so. Do not dress a guess as a rigorous process. Label the answer low-confidence.
- **In a specialized procedure the base model lacks, and it recurs:** build that procedure as a skill via `fable-domain`.

---

## Step 0 - Classify the Ask

| Shape | Signal | Deliverable |
|---|---|---|
| **Question / assessment** | "why is...", "what do you think...", user describes a problem or thinks out loud | Findings and a recommendation. Change nothing. |
| **Task** | "fix", "build", "change", "make" | The completed change, verified. |
| **Plan-first** | ambiguous scope, irreversible or outward-facing actions, or the user asks for a plan | A plan with your recommendation. Stop and wait for approval. |

Tie-breaks:
1. If any plan-first signal is present, plan-first beats task.
2. A mixed ask ("why is this failing, and can you fix it?") is a task whose final report must also answer the question.
3. Genuinely unsure between task and plan-first: choose plan-first.

---

## Step 1 - Define Done

Tell the user, in one or two sentences, what done looks like and how it will be verified:
- **Task:** concrete observation (test passes, build green, metric changes, file exists).
- **Question/assessment:** every claim in findings traces to something read or run (cited file:line or command output).
- **Plan-first:** a plan the user can approve, naming verification for each step.

State your load-bearing assumptions. If checkable with a single tool call, check it instead of assuming.

---

## Step 2 - Gather Evidence

1. **Orient first.** Enumerate what exists (list directory, glob project) before reading specifics.
2. **Primary sources beat memory.** Read actual code, files, and outputs. Fetch current library docs.
3. **Parallelize independent lookups.** Web fetches, doc lookups, subagents in one parallel batch.
4. **Read narrow, never re-read.** Search for relevant sections; quote load-bearing lines only.
5. **Time-box mechanically.** Two lookup rounds maximum unless a third has a stated reason.
6. **Establish intent before changing behavior.** Confirm code, check, and spec agree.
7. **Surprises route the loop.** Contradictions to expectations must be stated and re-routed.

---

## Step 3 - Decide and Commit

Synthesize evidence into **one recommendation**. Name alternatives in one line each if considered.
Reversibility test: actions visible to others or systems (push, publish, send, deploy, delete shared data) are irreversible and require explicit user authorization.

**Authorization Gate:**
`AUTH: user said "<their exact words>"`
If no exact quote exists, do not take the outward/irreversible action; list it as a pending step requiring authorization.

---

## Step 4 - Act Surgically

1. **Intent Gate:** Write verbatim line before behavior-changing edit:
   `INTENT: code does <X>; failing check/task expects <Y>; spec (README/docs) says <Z>`
2. **Recall Gate:** Never write API signatures, endpoints, or config keys from memory.
3. **Smallest correct change:** Touch only what the task requires.
4. **Precise edits over rewrites:** Rewrite a file only if authored in this session or fully read.
5. **Track multi-part work:** Maintain a written checklist for 3+ items.
6. **Never destroy without looking:** Inspect before overwriting or deleting.
7. **Failed-edit recovery:** Re-read exact region, adjust match, retry once before widening scope.

---

## Step 5 - Verify by Observation

Verification requires three components:
- **(a)** Done criterion passes, directly observed.
- **(b)** Surrounding system health maintained (build, lint, adjacent tests).
- **(c) Twin Check:** Whenever fixing a defect, search the codebase for identical wrong constructs and report:
  `TWINS: searched <pattern> - found <N> other sites: <files or "none">`

Hard bound: After 3 failed fix-verify cycles on the same issue, stop and report hypothesis.

---

## Step 6 - Report Outcome-First

- First sentence answers what happened or what was found.
- Plain language first, technical details second.
- Mandatory gate lines when applicable:
  - `INTENT:` line if behavior changed.
  - `AUTH:` line if outward action taken.
  - `PENDING:` line if prescribed follow-up deferred.
  - `TWINS:` line if defect fixed.
- Delete scratch files and temporary debris before reporting.
