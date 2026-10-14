# Domain procedure

Inputs: Synthetic or authorized fixture data, redaction policy, output surfaces and expected safe representation.

Outputs: Leakage/over-redaction findings, sanitized evidence and remediation checks.

1. Identify sensitive classes and every requested output/log/export surface.
2. Prefer synthetic fixtures; never persist live credentials in evidence or chat.
3. Exercise the actual redaction path where available and inspect both content and diagnostic output.
4. Compare against policy-required masking while retaining allowed context; report unsupported surfaces as unverified.

Verification: apply the supplied domain contract to actual outputs; record source/version and executed check results. Missing required evidence, interface or permission blocks its dependent step. AGENTS.md governs; no independent agent identity or runtime installation is implied.
