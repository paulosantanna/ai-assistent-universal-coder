# Quality Checklist

Use this checklist at the end of the Validate phase to ensure the skill
meets all quality criteria before delivery.

---

## Structural Checks (Pass/Fail)

These are hard requirements. Any failure must be fixed.

- [ ] SKILL.md exists with exact casing
- [ ] YAML frontmatter has opening and closing `---` delimiters
- [ ] `name` field is present and kebab-case
- [ ] `name` matches the folder name
- [ ] `description` field is present
- [ ] `description` is under 1024 characters
- [ ] `description` contains no XML angle brackets (< >)
- [ ] `name` does not contain "claude" or "anthropic"
- [ ] No README.md inside the skill folder
- [ ] Folder name is kebab-case (no spaces, no capitals, no underscores)

## Description Quality (Score 1-5)

Rate each and target 4+ on all:

- [ ] **Specificity (1-5):** Does it describe a concrete capability?
- [ ] **Trigger clarity (1-5):** Would the agent know when to load this?
- [ ] **User language (1-5):** Does it use phrases a user would actually say?
- [ ] **Scope boundaries (1-5):** Is it clear what this skill does NOT do?
- [ ] **Pushiness (1-5):** Is it assertive enough to avoid undertriggering?

## Instruction Quality (Score 1-5)

- [ ] **Actionability (1-5):** Can the agent follow every step without ambiguity?
- [ ] **Specificity (1-5):** Are instructions concrete (not "validate properly")?
- [ ] **Examples (1-5):** Are there realistic input/output examples?
- [ ] **Error handling (1-5):** Are common failures addressed?
- [ ] **Progressive disclosure (1-5):** Is SKILL.md focused, with details in refs?
- [ ] **Composability (1-5):** Does it play well with other skills?

## Trigger Testing

### Should trigger (test 3-5 phrases)

1. [ ] "[Obvious request]" → triggers? Y/N
2. [ ] "[Paraphrased request]" → triggers? Y/N
3. [ ] "[Informal request]" → triggers? Y/N

### Should NOT trigger (test 3-5 phrases)

1. [ ] "[Unrelated task]" → stays silent? Y/N
2. [ ] "[Similar but different scope]" → stays silent? Y/N
3. [ ] "[Generic question]" → stays silent? Y/N

## Performance Targets

Aspirational benchmarks (adapt to your skill):

- [ ] Triggers on ≥90% of relevant queries
- [ ] Completes workflow without user correction
- [ ] Consistent results across separate sessions
- [ ] No failed tool/API calls per workflow
- [ ] Users don't need to prompt the agent about next steps

## Final Sign-Off

- [ ] User has reviewed the skill
- [ ] Test phrases produce expected behavior
- [ ] Skill is packaged and ready for upload

## Workspace grading rubric (0–100)

Updated: 2026-10-13. Local operational rubric implementing the scoring requirement visible in IMG_2714; the photographed rubric itself was not supplied.

| Dimension | Weight | Evidence required |
| --- | --- | --- |
| Routing | 20 | concrete outcome, positive phrases, negative boundary, distinction from siblings |
| Procedure | 25 | ordered actionable steps, decisions, inputs, outputs, stop condition |
| Examples | 15 | realistic request/actions/result pairs and a boundary example |
| Errors and safety | 15 | realistic failure handling, permissions, secrets, no fictional tools |
| Disclosure and composition | 15 | <=100 physical entry lines, links/load conditions, intact needed resources |
| Verification and provenance | 10 | runnable checks, source/license/version and truthful evidence scope |

Rate each dimension 0–5, with evidence: 0 absent, 1 vague, 2 partial, 3 usable with gaps, 4 specific and complete, 5 also verified by applicable behavior/routing evidence. Contribution = weight × rating / 5. Round the sum to one decimal. Any structural error caps the result at 49/100 and keeps status FAIL. Missing evidence cannot receive 5. State manual trigger review separately from an actual harness evaluation; the score is a diagnostic, not release authorization.
