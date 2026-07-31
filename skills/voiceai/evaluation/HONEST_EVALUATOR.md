# HONEST_EVALUATOR.md

Use this checklist before marking `voiceai` work complete.

## Evidence Review

- Was audio capture consent explicit and scoped to the current session?
- Is the literal transcript preserved separately from the actionable brief?
- Are mixed-language spans tagged without forcing one language for the whole utterance?
- Are jokes, small talk and out-of-scope content preserved but excluded from execution?
- Does each actionable requirement cite source transcript segments?
- Are privacy, retention, tool and evidence limitations stated?
- Did any output route around AEOS handoff, approval, registry or generator governance?

## Verdict Rules

- Return `PASS` only when transcript, classification, handoff and evidence requirements are satisfied.
- Return `REVIEW` when the output is useful but needs human confirmation of ambiguous speech, language spans or intent.
- Return `BLOCKED` when consent, tool access, audio quality, retention policy, evidence or approval is missing.
