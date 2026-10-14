# Domain procedure

Inputs: User objective, available skills/tools, permissions and target project constraints.

Outputs: Ordered playbook, step input/output contracts, dependency/resource sets and stop/completion conditions.

1. Translate the objective into bounded observable steps using existing capabilities.
2. Declare inputs, outputs, dependencies, allowed tools and required evidence for each step.
3. Keep specialization in skills/lenses; use the canonical lifecycle and never introduce worker agent identities.
4. Check missing dependencies, conflicts and acceptance gates; validate the playbook format against the actual consumer before execution.

Verification: apply the supplied domain contract to actual outputs; record source/version and executed check results. Missing required evidence, interface or permission blocks its dependent step. AGENTS.md governs; no independent agent identity or runtime installation is implied.
