# Domain procedure

Inputs: Reusable task, target workspace, inspected capabilities/resources and explicit constraints.

Outputs: Reviewable SKILL.md, necessary local modules, provenance and validation report.

1. Use the current skill-factory and skill-architect contracts rather than inventing a scaffold.
2. Define positive/negative routing, inputs, outputs, risks and evidence requirements.
3. Keep the entrypoint at most 100 physical lines and preserve substantive procedures in local modules.
4. Validate actual resources and discovery metadata; do not claim generated instructions install missing runtime services.

Verification: apply the supplied domain contract to actual outputs; record source/version and executed check results. Missing required evidence, interface or permission blocks its dependent step. AGENTS.md governs; no independent agent identity or runtime installation is implied.
