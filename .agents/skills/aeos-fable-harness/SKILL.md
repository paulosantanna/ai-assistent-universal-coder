---
name: aeos-fable-harness
description: Universal execution harness wrapping all AEOS skills with the Fable Method problem-solving loop, Fit Gate, Intent Gate, Recall Gate, Twin Check, and adversarial Fable Judge pass.
---

# Enterprise Skill: aeos-fable-harness

## Mission

Enforce Fable Method governance across ALL AEOS skills inside AEOS v1.1.

## Production Scope

This harness wraps every AEOS skill execution (`aeos-*` and core skills) in the Fable 6-step loop:
1. **Classify Ask & Define Done** (Question/Assessment, Task, Plan-first)
2. **Evidence Gathering** (Primary sources first, minimal evidence set)
3. **Decide & Commit** (Authorization Gate for outward actions)
4. **Surgical Execution** (Intent Gate & Recall Gate)
5. **Observed Verification** (Target check + Surrounding health + Twin Check)
6. **Outcome-First Report & Adversarial Fable Judge Pass**

## Allowed Actions

- Intercept and wrap AEOS skill invocations.
- Enforce Tool Router, evidence verification, and Fable Judge audit.
- Generate evidence-backed artifacts and reports.

## Forbidden Actions

- Bypassing Fable gates (Fit Gate, Intent Gate, Auth Gate, Twin Check).
- Accepting unverified skill outputs.
- Secret, token, or key exposure.

---

# Execution Harness Protocol

When any AEOS skill is invoked:
1. **Load Domain Adapter:** Match the target skill to its Fable domain adapter (`references/domains/aeos-skills-domain.md`).
2. **Execute Fit & Triviality Gates:** Verify if the task is trivial or requires full loop.
3. **Execute Skill under Fable Loop:**
   - Write `INTENT:` line before behavior edits.
   - Execute `AUTH:` line check for outward/irreversible actions.
   - Run double verification (target + surrounding system).
   - Execute `TWINS:` search for bug fixes.
4. **Adversarial Pass:** Run `aeos-fable-judge` over the result before final submission.
