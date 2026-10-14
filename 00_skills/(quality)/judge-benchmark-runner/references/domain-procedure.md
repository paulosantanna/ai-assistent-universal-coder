# Domain procedure

Inputs: Judge service/CLI contract, benchmark corpus, expected decisions and frozen thresholds.

Outputs: Per-case actual/expected decisions, requested metrics, reproducibility metadata and threshold result.

1. Verify the deterministic gate interface, version and corpus integrity.
2. Freeze expected decisions and thresholds before invoking the actual gate.
3. Run eligible cases and preserve sanitized outputs; report unavailable runtime as blocked.
4. Summarize false approvals/rejections and requested performance metrics; do not replace the gate with a persona or revise failed expectations.

Verification: apply the supplied domain contract to actual outputs; record source/version and executed check results. Missing required evidence, interface or permission blocks its dependent step. AGENTS.md governs; no independent agent identity or runtime installation is implied.
