# Domain procedure

Inputs: Candidate answer/artifact, authorized source corpus and acceptance criteria.

Outputs: Claim-to-source matrix, grounded/contradicted/unverified labels, bounded corrections and evidence references.

1. Extract independently checkable claims without changing their meaning.
2. Resolve each claim against the supplied evidence; distinguish absence of evidence from contradiction.
3. Check quotation fidelity, source applicability and version/date mismatches.
4. Report unsupported claims and omitted material facts; propose corrections only when the source supports them.

Verification: apply the supplied domain contract to actual outputs; record source/version and executed check results. Missing required evidence, interface or permission blocks its dependent step. AGENTS.md governs; no independent agent identity or runtime installation is implied.
