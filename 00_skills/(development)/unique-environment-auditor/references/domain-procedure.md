# Domain procedure

Inputs: Authorized workspace/environment inventory, manifests and required runtime/tool constraints.

Outputs: Evidence-based compatibility/conflict matrix, missing requirements and bounded remediation plan.

1. Inspect declared versions, lockfiles, tool paths and workspace configuration without reading secret contents.
2. Compare declared and observed runtimes; distinguish absence from conflicting duplicate installations.
3. Check which environment each documented command actually targets.
4. Report conflicts with source pointers and minimal remediation; do not alter global tools or assert uniqueness without complete evidence.

Verification: apply the supplied domain contract to actual outputs; record source/version and executed check results. Missing required evidence, interface or permission blocks its dependent step. AGENTS.md governs; no independent agent identity or runtime installation is implied.
