# Domain procedure

Inputs: Corpus manifest, schema, licensing/provenance requirements and expected-output definitions.

Outputs: Corpus validation report with missing/duplicate/invalid cases, hashes and eligibility decisions.

1. Resolve every manifest entry and check unique IDs and declared hashes.
2. Validate input/output shape and required labels against the supplied schema.
3. Check provenance, permissions and secret/private-data constraints without printing raw sensitive values.
4. Flag orphaned, ambiguous or unverifiable cases; preserve the corpus and do not invent expected outputs.

Verification: apply the supplied domain contract to actual outputs; record source/version and executed check results. Missing required evidence, interface or permission blocks its dependent step. AGENTS.md governs; no independent agent identity or runtime installation is implied.
