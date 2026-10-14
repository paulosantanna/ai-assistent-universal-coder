# Existing-skill review

Updated: 2026-10-13
Entry point: ../SKILL.md. Source: IMG_2714–IMG_2715.

1. Inspect the actual package and callers; run validate_skill.py before edits. Save its report and baseline hashes.
2. Apply the rubric in quality-checklist.md with cited package evidence. Structural pass is separate from quality. Do not guess a score from line count.
3. Diagnose weak triggers, missing examples, buried invariants, swallowed errors, excessive entry size and broken/host-specific references.
4. Define what better means using the existing request. Extract scope from history; ask only if the unknown blocks safe work.
5. Apply the smallest reversible fix. Preserve functioning modes, attribution, resource bytes and invocation fields. Rerun checks appropriate to the changed behavior.
6. Report before/after scores, validation result, changed behavior and unverified runtime dependencies. Never rewrite a functioning skill merely to impose a template.

Examples: “rate my skill” → read-only report and evidence-backed grade; “improve the missing trigger” → scoped description/caller synchronization; “turn this into a skill” → discovery/architecture before generation.
Failure: unavailable caller/source → assess only inspected scope and label the missing evidence; invalid YAML → structural FAIL and grade cap, fix only if correction is authorized.
