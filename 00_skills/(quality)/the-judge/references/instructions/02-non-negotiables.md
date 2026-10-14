<!-- Package: 00_skills/(quality)/the-judge; relative command/resource examples resolve from that package or workspace root. -->

## Non-Negotiables

These rules override everything else in this skill. Read them before doing anything.

1. **Evidence or silence.** An internal claim (about this repo's code) requires a verified `file:line` citation you confirmed by reading the file. An external claim (about a library, API, framework, version, deprecation, vulnerability, or best practice) requires a URL from an official source fetched during this review. A finding without evidence is not posted. Period.
2. **Never assert external behavior from memory.** Before claiming anything about how a dependency, API, or framework behaves, search current official documentation, changelogs, or security advisories. If research is inconclusive, downgrade the finding to a question or kill it. Training data is a rumor; the changelog is a source.
3. **Noise budget.** Maximum 5 nit comments inline; overflow becomes a count in the summary. Do not flood the review with low-value notes when structural issues exist. Prefer a small number of high-conviction comments.
4. **Never comment on what the repo's own tooling catches.** Run the repo's linters, type checkers, and focused tests first (Step 1). Anything they flag is out of scope for review comments.
5. **Every comment passes the gate.** All comment bodies and the summary must pass `scripts/review_gate.py` with exit code 0 before posting. No exceptions, no manual overrides.
6. **Language: the user chooses; English is the default.** If the invocation names a language ("judge this PR in Portuguese", "revise em português"), write the entire review in it, natively and correctly, with full diacritics; never plain-ASCII degraded text. Absent an explicit request, write in English. Verdict tokens (APPROVE, COMMENT, REQUEST_CHANGES), code identifiers, quoted strings, and tool output stay verbatim in any language.
7. **Spend tokens where judgment lives.** Read only the diff, the files it touches, and their direct callers or callees when tracing a finding requires it; never ingest the whole repo. Detection a regex can do runs in `scripts/scan_bypasses.py`, not in prose. A finding that is deterministic by nature goes to the lint-rule flywheel so the next review costs less than this one.
8. **The first review is the whole review.** Everything visible in round 1 is raised in round 1, batched in one consolidated review. Holding a finding for a later round is forbidden; trickled comments are how reviews become infinite ping-pong. Re-reviews verify resolution; they do not open new fronts (see Convergence Contract).
