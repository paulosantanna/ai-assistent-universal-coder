# Domain procedure

Inputs: Policy contract, authorized defensive scenarios, actual enforcement interfaces and expected decisions.

Outputs: Scenario-to-policy matrix, observed allow/deny outcomes, evidence and uncovered boundaries.

1. Identify the protected operation, caller authority and expected deny/allow conditions.
2. Design bounded scenarios for scope, identity, expiry and evidence bypass using the supplied contract.
3. Exercise available authorized enforcement surfaces; report unavailable paths as untested.
4. Preserve denied outcomes and failed checks; propose policy fixes without disabling enforcement or treating an evaluator as approval.

Verification: apply the supplied domain contract to actual outputs; record source/version and executed check results. Missing required evidence, interface or permission blocks its dependent step. AGENTS.md governs; no independent agent identity or runtime installation is implied.
