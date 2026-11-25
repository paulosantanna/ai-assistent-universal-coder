# Procedure

## Contents

- TLC gates
- Adapted upstream instructions
- Upstream modules

## TLC gates

These gates win when the adapted text disagrees.

- Sibling product skills that are not in this workspace are missing. Name them and stop. Do not fetch or execute remote skill bodies unless the user asks to import that sibling.
- Confirm container image, GPU time, and output directory before a run.
- Do not treat a rendered or reconstructed scene as measured sensor truth.
- Missing source, tool, permission, or checkout blocks the dependent step. Continue only independent authorized work.
- Do not create another agent identity. A role in the upstream text is a lens of `codenavi-agent`.

## Adapted upstream instructions

# CAD to SimReady

## When to Use

Use this workflow skill for an end-to-end pipeline from a source asset to a
SimReady asset or package. It coordinates existing conversion, authoring,
validation, conformance, rendering, and packaging references directly; do not
replace it with a single monolithic runner command.

This skill is documentation-driven and does not ship `scripts/run.py`; it must
not depend on a repository checkout. `Shell` is declared because this workflow
invokes installed stage reference scripts directly, from each reference's
installed directory, and it still must not grow a monolithic runner.

## Prerequisites

- Prefer `preflight` first for deterministic setup: it installs/verifies
  local upstream checkouts, writes a `cad-to-simready-preflight.json`
  manifest, and exports `PHYSICAL_AI_PREFLIGHT_MANIFEST` plus
  `PHYSICAL_AI_REQUIRE_PREFLIGHT=1` for downstream references.
- Python 3.12 and `uv` (per repo `README.md`).
- A Content Agents model provider key when local deployment will run, or
  explicit endpoint variables plus usage tokens for already-running
  endpoints; see `references/preflight/README.md` for the full list.
- Docker, NVIDIA Container Toolkit, and an NVIDIA GPU for Content Agents and
  OVRTX stages.
- Local upstream checkouts under
  `${OMNIVERSE_CAD_TO_SIMREADY_UPSTREAM_ROOT:-$HOME/.omniverse-cad-to-simready/upstreams}`
  when a stage needs upstream scripts or specs.

## First Action

For any broad CAD/source-asset to SimReady request, assume
`property_assignment_intent=run` unless the user explicitly asks for
conversion-only, validation-only, or no material/physics assignment.
For conversion-only requests, set `property_assignment_intent=skip`, do not
deploy Content Agents, run `convert-to-usd`, then run `validate-usd-minimum`
on the generated USD if conversion succeeds. For validation-only requests,
set `property_assignment_intent=skip` and validate the USD the user
provided without rerunning conversion.

Run `preflight` (or verify an existing `PHYSICAL_AI_PREFLIGHT_MANIFEST`)
before any converter, validation, Content Agents, OVRTX, packaging, or FET
step; treat it as dependency bootstrap, not workflow routing. Use
`--skip-content-agents` for conversion-only/validation-only requests.

When `property_assignment_intent=run`, verify or deploy Content Agents
services immediately after confirming the source path and resolving intent,
before asset-context inspection, converter dependency checks, conversion,
validation, conformance, rendering, packaging, or upstream source builds.
Treat explicitly provided healthy endpoints as user-owned; otherwise run `deploy-content-agents`,
which deploys the shared standalone OVRTX renderer, then Material, Physics,
and optional Texture service containers in order.

## Instructions

1. Confirm the source asset path exists, resolve `output_root`, and classify
   the request as end-to-end, conversion-only, validation-only, or packaging.
2. Resolve `property_assignment_intent` before running any asset inspection,
   converter probe, conversion, validation, conformance, rendering, or
   packaging step.
3. Run `preflight` for the selected workflow targets, unless a ready
   `PHYSICAL_AI_PREFLIGHT_MANIFEST` is already configured. Source the generated
   env file before running downstream scripts. Treat preflight as dependency
   setup only: it may use a provided `--source-asset`, `--source-format`, or
   `--conversion-tools` value to scope dependency checks, but `convert-to-usd`
   and the upstream converter references still decide actual conversion support.
4. Verify or deploy Content Agents services first when
   `property_assignment_intent=run`; block on missing authentication or
   unhealthy services instead of continuing.
5. Read `references/workflow.md` and `references/commands.md`, then run only
   the stage references needed for the current request.
6. Run `identify-asset-context` on the original source asset when web search is
   available or property assignment will run.
7. Route the source through `convert-to-usd`, or skip conversion for existing
   USD input and treat the source path as the current USD path.
8. Run `validate-usd-minimum` before expensive downstream work. Treat this as a
   viability gate only: record unit/profile issues such as `metersPerUnit !=
   1.0`, but do not run `simready-conform-profile`, FET001, or any other FET
   repair before Content Agents assignment when property assignment will run.
9. Run Content Agents material, physics, and optional texture assignment on the
   converted/minimum-valid USD when requested or required.
10. Run `simready-conform-profile` on the latest simulation USD path after
   property assignment and preserve every selected FET repair report.
11. Run validation gates in order: `omni-asset-validate`,
   `omni-asset-validate-geometry`, `omni-asset-validate-physics`, and
   `simready-validate`.
12. Rerun `simready-conform-profile` when `simready-validate` reports a
    repairable requirement, then rerun profile validation on the newest authored
    USD.
13. Run `ovrtx-render-service` when preview, thumbnail, or inspection images
    are requested. When package outputs are requested, run
    `assemble-package-source` next to create the clean `deliverable/` package
    source from the final USD and thumbnail, then run `nv-core-package-sample`
    and `nv-core-package-sample-validation` on that deliverable folder only.
14. Emit the consolidated workflow report with the final USD path, all stage
    reports, validation findings, rerun reasons, and next work.

## Output Format

Emit a consolidated workflow report in Markdown, and include JSON when the
workflow writes structured artifacts. Report overall status as `passed`,
`blocked`, `failed`, or `needs_rerun`. See `references/workflow.md` for the
required Markdown and JSON report fields.

## Detailed References

Read only the references needed for the current request:

- `references/preflight/README.md`: deterministic local setup, manifest/env
  contract, wrappers, deployment opt-out, and guardrail behavior.
- `references/workflow.md`: inputs, source routing, detailed workflow,
  validation policy, output report fields, and next steps.
- `references/commands.md`: concrete portable script command patterns.
- `references/assemble-package-source/README.md`: two-zone package source
  assembly, root USD naming, thumbnail placement, and deliverable checks.
- `references/troubleshooting.md`: symptom/cause/fix table plus FET
  (`GSP.001`/`RB.MB.001`) repair-routing detail.
- `references/publishing-layout.md`: frontmatter compatibility-field notes and
  layout rationale for this skill's own file tree.

## Publishing Layout Notes

Use `skills/omniverse-cad-to-simready/` as the source of truth for this
product repo's skill. The `.agents/skills` symlink is a compatibility alias
for local agentskills.io-style discovery, and the nested `references/` tree
is intentional. See `references/publishing-layout.md` for the alias list,
frontmatter field placement, and flattening rules.

## Limitations

- This workflow coordinates existing conversion, property assignment,
  conformance, validation, rendering, and packaging skills; it does not replace
  them with a single monolithic runner command.

## Troubleshooting

Read `references/troubleshooting.md` only when a specific stage or validation
gate is failing; it owns the symptom/cause/fix table and FET repair routing.

## Hard Rules

- Prefer the preflight manifest for local upstream roots, converter
  executables, SimReady validation runtime, OVRTX endpoint, and Content Agents
  service URLs. When `PHYSICAL_AI_REQUIRE_PREFLIGHT=1` is set, do not bypass the
  manifest with direct upstream discovery.
- Do not run asset inspection, converter probes, local upstream builds,
  conversion, validation, conformance, rendering, or packaging before Content
  Agents readiness when property assignment will run.
- Use stage-specific installed reference scripts directly. Do not add or call a
  single `omniverse-cad-to-simready` runner command.
- For source conversion, delegate to the `convert-to-usd` reference; do not
  substitute another converter for CAD or mesh formats.
- For property assignment, use Content Agents references as separate atomic steps:
  material first, then physics, then texture only when requested.
- When property assignment will run, do not run `simready-conform-profile` or
  any FET helper before Content Agents. Validate minimum USD first, then run
  Content Agents on that converted/minimum-valid USD, then apply FET repairs to
  the latest service-authored USD.
- When property assignment will run, do not run `simready-validate` or any
  SimReady profile validation before Content Agents. The only validation gate
  allowed before service calls is `validate-usd-minimum`, which is a basic USD
  viability check.
- Stop at the first failing deployment, conversion, property-assignment, or
  conformance authoring gate unless the user explicitly asks for best-effort
  continuation.
- Do not stop at validation findings after a meaningful USD artifact exists.
  Continue remaining diagnostic gates and mark the result `needs_rerun`.
- Do not leave a `GSP.001` profile failure as an unclassified final finding.
  Route it to upstream `simready-foundation-conform-fet-005-simulate-grasp-physics`; if
  the current agent cannot inspect renders or no explicit grasp points are
  available, report a blocked FET005 repair with the visual evidence path or
  missing input reason.
- Preserve every stage report and pass the concrete output USD path from each
  report into the next stage.

## Upstream modules

Read a module only when the request matches that mode.

- [CHANGELOG.md](upstream/CHANGELOG.md)
- [references/assemble-package-source/README.md](upstream/assemble-package-source/README.md)
- [references/commands.md](upstream/commands.md)
- [references/content-agents/README.md](upstream/content-agents/README.md)
- [references/content-agents/references/material-agent-client/README.md](upstream/content-agents/references/material-agent-client/README.md)
- [references/content-agents/references/physics-agent-client/README.md](upstream/content-agents/references/physics-agent-client/README.md)
- [references/content-agents/references/texture-agent-client/README.md](upstream/content-agents/references/texture-agent-client/README.md)
- [references/convert-to-usd/README.md](upstream/convert-to-usd/README.md)
- [references/convert-to-usd/references/mujoco-usd-converter/README.md](upstream/convert-to-usd/references/mujoco-usd-converter/README.md)
- [references/convert-to-usd/references/openusd-exchange-sdk-usdex/README.md](upstream/convert-to-usd/references/openusd-exchange-sdk-usdex/README.md)
- [references/convert-to-usd/references/urdf-usd-converter/README.md](upstream/convert-to-usd/references/urdf-usd-converter/README.md)
- [references/convert-to-usd/references/usd-convert-cad/README.md](upstream/convert-to-usd/references/usd-convert-cad/README.md)
- [references/convert-to-usd/references/usd-convert-gsplat/README.md](upstream/convert-to-usd/references/usd-convert-gsplat/README.md)
- [references/deploy-content-agents/README.md](upstream/deploy-content-agents/README.md)
- [references/deploy-content-agents/references/deploy-material-agent-docker.md](upstream/deploy-content-agents/references/deploy-material-agent-docker.md)
- [references/deploy-content-agents/references/deploy-ovrtx-docker.md](upstream/deploy-content-agents/references/deploy-ovrtx-docker.md)
- [references/deploy-content-agents/references/deploy-physics-agent-docker.md](upstream/deploy-content-agents/references/deploy-physics-agent-docker.md)
- [references/deploy-content-agents/references/deploy-texture-agent-docker.md](upstream/deploy-content-agents/references/deploy-texture-agent-docker.md)
- [references/identify-asset-context/README.md](upstream/identify-asset-context/README.md)
- [references/nv-core-package-sample-validation/README.md](upstream/nv-core-package-sample-validation/README.md)
- [references/nv-core-package-sample/README.md](upstream/nv-core-package-sample/README.md)
- [references/omni-asset-validate-geometry/README.md](upstream/omni-asset-validate-geometry/README.md)
- [references/omni-asset-validate-physics/README.md](upstream/omni-asset-validate-physics/README.md)
- [references/omni-asset-validate/README.md](upstream/omni-asset-validate/README.md)
- [references/ovrtx-render-service/README.md](upstream/ovrtx-render-service/README.md)
- [references/preflight/README.md](upstream/preflight/README.md)
- [references/publishing-layout.md](upstream/publishing-layout.md)
- [references/simready-conform-profile/README.md](upstream/simready-conform-profile/README.md)
- [references/simready-conform-profile/references/FET_000_CORE/README.md](upstream/simready-conform-profile/references/FET_000_CORE/README.md)
- [references/simready-conform-profile/references/FET_001_MINIMAL/README.md](upstream/simready-conform-profile/references/FET_001_MINIMAL/README.md)
- [references/simready-conform-profile/references/FET_004_SIMULATE_MULTI_BODY_PHYSICS/README.md](upstream/simready-conform-profile/references/FET_004_SIMULATE_MULTI_BODY_PHYSICS/README.md)
- [references/simready-conform-profile/references/FET_005_SIMULATE_GRASP_PHYSICS/README.md](upstream/simready-conform-profile/references/FET_005_SIMULATE_GRASP_PHYSICS/README.md)
- [references/simready-validate/README.md](upstream/simready-validate/README.md)
- [references/troubleshooting.md](upstream/troubleshooting.md)
- [references/validate-usd-minimum/README.md](upstream/validate-usd-minimum/README.md)
- [references/workflow.md](upstream/workflow.md)
