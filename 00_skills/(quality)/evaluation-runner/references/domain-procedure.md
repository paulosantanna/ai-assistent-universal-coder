# Domain procedure

Inputs: Evaluation contract, immutable fixture IDs, runner/version, thresholds and authorized execution scope.

Outputs: Case-level observations, aggregate metrics, execution metadata and blocking conditions.

1. Freeze expected outcomes and thresholds from the supplied contract before the run.
2. Verify fixture integrity and runner availability; missing execution infrastructure blocks execution.
3. Invoke the documented runner and retain sanitized raw observations and exit codes.
4. Calculate only requested metrics; report failures without editing fixtures or expectations to obtain a pass.

Verification: apply the supplied domain contract to actual outputs; record source/version and executed check results. Missing required evidence, interface or permission blocks its dependent step. AGENTS.md governs; no independent agent identity or runtime installation is implied.
