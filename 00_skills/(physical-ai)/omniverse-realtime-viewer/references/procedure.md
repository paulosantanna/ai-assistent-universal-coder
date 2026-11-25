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

<!-- SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved. -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Omniverse Realtime Viewer

Build responsive USD viewers by composing OVRTX rendering, OVStage scene state,
and the delivery/UI libraries appropriate to the app. Use this package for
viewer architecture and interaction; use each selected SDK's upstream guidance
for installation and exact release-specific APIs.

## Start With The App

1. When delivery is explicit, select its recipe through
   `references/routing.md` and follow its current phase. Otherwise start with
   `references/usd-viewer-app/README.md`. For an existing app, keep its
   architecture and read only the references for the requested change.
   Broad app, conventions and UI catalogs are lookups as needed.
2. Resolve the selected libraries through `references/dependencies/README.md`.
   Preserve the project's manifest unless an upgrade is requested.
3. Build a working frame and camera interaction in the chosen shell, then add
   the requested capabilities. Read `references/conventions.md` for shared input,
   camera, selection, and protocol conventions.
4. Use `references/viewer-ux-workflow/README.md` for broader interface design.
   Loading, selection feedback, errors, and input responsiveness belong in the
   first working app, alongside rendering.
5. Validate the actual delivery path with `references/validation.md`. A browser
   screenshot does not validate a native window or a different transport.

## Architecture

| Owner | Responsibility |
|---|---|
| Viewer runtime | Own the live OVStage, publication clock, OVRTX renderer, scene changes, and render stepping. |
| UI and input adapter | Display frames and copied app state; send user intent to the runtime owner. |
| Storage/query/simulation workers | Perform their assigned work and return results through the selected integration boundary. |
| Delivery adapter | Present locally or stream through ovstream; respect frame ownership and backpressure. |

Use OVRTX for USD/3D rendering. Browser apps display its WebRTC video; local apps
present its output through their native shell. A missing GPU means rendering is
unverified, not a reason to substitute a browser 3D renderer.

Keep viewer cameras, settings, effects, and transient edits in app-owned session
or runtime state so the source USD stays intact. Serialize scene mutation and
render stepping through the runtime owner. Read
`references/ovstage-ovrtx-integration/README.md` for that loop, then the population
or data-plane references when implementing scene loading or attribute writes.

Keep expensive loading and metadata work off the UI and render threads. Keep
transport details behind a delivery adapter so camera, selection, properties,
and loading state can be reused across local and streamed shells.

## Add Capabilities As Needed

Use `references/routing.md` to select camera/picking, scene management, render
settings, cloud assets, simulation, editor tools, deployment, or CAE/CFD
visualization. Read the selected capability's implementation flow and its linked
contract; the full reference catalog is not a prerequisite for a first frame.

For simulation, use the routing reference's Simulation Ecosystem section plus
`references/realtime-sim-integration/README.md`. For UI-driven forces or control,
add `references/interaction-round-trip/README.md`.

For example scenes, use `references/usd-sample-data/README.md`. When a runtime
failure needs diagnosis, use `references/troubleshooting/README.md` and the
selected SDK's matching release guidance before changing the architecture.

## Solid Modeling: Upstream First

For usd-brep, exact BRep, solid modeling, kernel failures, CAD topology, or
BrepArray questions, first read `references/dependencies/README.md` → USD BRep. Follow the
owning repository's current agent guidance, skills, operation docs, and package
API before selecting local integration references. Discover the upstream router
rather than assuming skill names or directory layouts remain fixed. Upstream
owns modeling semantics, schema rules, tuning, and diagnostics; this package
owns OVRTX display, worker handoff, selection mapping, and publication timing.

## GPU Processing And Stylized Viewers

For custom GPU processing, chained outputs and lens sampling, read
`references/spg-processing/README.md`. For toon, ink, technical/X-Ray styles,
geometry strokes or full wireframe, continue to
`references/stylized-visualization/implementation.md`. Its USD/Lua/CUDA starting
node and geometry/depth/composite build sequence work with the selected viewer
recipe; use `references/stylized-visualization/style-recipes.md` for the preset
math and `references/stylized-visualization/README.md` for supporting contracts.
Implement the result inside the existing OVRTX/runtime owner and deliver the
published processed output. These instructions do not require a sample checkout
or a prior stylized-rendering implementation.

For an optional usd-brep geometry source, first read
`references/dependencies/README.md` → USD BRep and the owning repository's
current agent guidance, skills, and operation docs; then read
`references/stylized-visualization/usd-brep-source.md` for the display boundary.

## XR Viewers

For headsets, immersive viewers, or spatial editors, start with
`references/xr-viewer-recipe/README.md`. Resolve SDK setup and contracts through
`references/dependencies/ovxr.md`; the library owns OpenXR lifecycle and frame
submission. For controllers, hands, navigation, or scene tools, add
`references/xr-spatial-input/README.md` and
`references/ovxr-python-interactions/README.md`. For projection-integrated UI,
read `references/ovxr-composition-ui/README.md` and
`references/ovxr-composition-ui-validation/README.md`.

## Upstream modules

Read a module only when the request matches that mode.

- [references/a2ui-scene-copilot/README.md](upstream/a2ui-scene-copilot/README.md)
- [references/aov-switching/README.md](upstream/aov-switching/README.md)
- [references/cae-cfd-visualization/README.md](upstream/cae-cfd-visualization/README.md)
- [references/cae-cfd-visualization/cae-data-ingestion.md](upstream/cae-cfd-visualization/cae-data-ingestion.md)
- [references/cae-cfd-visualization/coordinate-systems-and-up-axis.md](upstream/cae-cfd-visualization/coordinate-systems-and-up-axis.md)
- [references/cae-cfd-visualization/data-and-operators.md](upstream/cae-cfd-visualization/data-and-operators.md)
- [references/cae-cfd-visualization/driving-cae-viz-via-ovstage.md](upstream/cae-cfd-visualization/driving-cae-viz-via-ovstage.md)
- [references/cae-cfd-visualization/emitter-and-seed-sources.md](upstream/cae-cfd-visualization/emitter-and-seed-sources.md)
- [references/cae-cfd-visualization/glyphs.md](upstream/cae-cfd-visualization/glyphs.md)
- [references/cae-cfd-visualization/ovstage-render-and-camera.md](upstream/cae-cfd-visualization/ovstage-render-and-camera.md)
- [references/cae-cfd-visualization/ovui-controls.md](upstream/cae-cfd-visualization/ovui-controls.md)
- [references/cae-cfd-visualization/rtwt-blueprint-recreation.md](upstream/cae-cfd-visualization/rtwt-blueprint-recreation.md)
- [references/cae-cfd-visualization/streaming-cae-viewer.md](upstream/cae-cfd-visualization/streaming-cae-viewer.md)
- [references/cae-cfd-visualization/temporal-playback.md](upstream/cae-cfd-visualization/temporal-playback.md)
- [references/cae-cfd-visualization/usd-authoring-and-materials.md](upstream/cae-cfd-visualization/usd-authoring-and-materials.md)
- [references/cae-cfd-visualization/volume-rendering.md](upstream/cae-cfd-visualization/volume-rendering.md)
- [references/camera-auto-select/README.md](upstream/camera-auto-select/README.md)
- [references/camera-controls/README.md](upstream/camera-controls/README.md)
- [references/camera-picker/README.md](upstream/camera-picker/README.md)
- [references/cloud-assets/README.md](upstream/cloud-assets/README.md)
- [references/cloud-deployment/README.md](upstream/cloud-deployment/README.md)
- [references/cloud-deployment/container-image-build.md](upstream/cloud-deployment/container-image-build.md)
- [references/cloud-deployment/gpu-container-runtime.md](upstream/cloud-deployment/gpu-container-runtime.md)
- [references/cloud-deployment/nvcf-self-hosted.md](upstream/cloud-deployment/nvcf-self-hosted.md)
- [references/cloud-deployment/nvcf-viewer-container-contract.md](upstream/cloud-deployment/nvcf-viewer-container-contract.md)
- [references/cloud-deployment/webrtc-network-diagnostics.md](upstream/cloud-deployment/webrtc-network-diagnostics.md)
- [references/cloudxr-opaque-data-channel/README.md](upstream/cloudxr-opaque-data-channel/README.md)
- [references/conventions.md](upstream/conventions.md)
- [references/cpp-native-viewer/README.md](upstream/cpp-native-viewer/README.md)
- [references/cpp-native-viewer/build-details.md](upstream/cpp-native-viewer/build-details.md)
- [references/cpp-native-viewer/interaction-features.md](upstream/cpp-native-viewer/interaction-features.md)
- [references/cpp-native-viewer/presentation-loop.md](upstream/cpp-native-viewer/presentation-loop.md)
- [references/cpp-native-viewer/project-build.md](upstream/cpp-native-viewer/project-build.md)
- [references/cpp-native-viewer/renderer-session.md](upstream/cpp-native-viewer/renderer-session.md)
- [references/cpp-native-viewer/validation.md](upstream/cpp-native-viewer/validation.md)
- [references/dependencies/README.md](upstream/dependencies/README.md)
- [references/dependencies/electron-shm.md](upstream/dependencies/electron-shm.md)
- [references/dependencies/environment-validation.md](upstream/dependencies/environment-validation.md)
- [references/dependencies/frontend.md](upstream/dependencies/frontend.md)
- [references/dependencies/local-openusd-gpu.md](upstream/dependencies/local-openusd-gpu.md)
- [references/dependencies/nvidia-runtime.md](upstream/dependencies/nvidia-runtime.md)
- [references/dependencies/ovrtx.md](upstream/dependencies/ovrtx.md)
- [references/dependencies/ovstream.md](upstream/dependencies/ovstream.md)
- [references/dependencies/ovxr.md](upstream/dependencies/ovxr.md)
- [references/dependencies/quick-setup.md](upstream/dependencies/quick-setup.md)
- [references/dependencies/skia-yoga.md](upstream/dependencies/skia-yoga.md)
- [references/electron-shm-viewer/README.md](upstream/electron-shm-viewer/README.md)
- [references/electron-shm-viewer/architecture-project.md](upstream/electron-shm-viewer/architecture-project.md)
- [references/electron-shm-viewer/electron-client.md](upstream/electron-shm-viewer/electron-client.md)
- [references/electron-shm-viewer/protocol-interaction-lifecycle.md](upstream/electron-shm-viewer/protocol-interaction-lifecycle.md)
- [references/electron-shm-viewer/python-shm-server.md](upstream/electron-shm-viewer/python-shm-server.md)
- [references/electron-shm-viewer/validation.md](upstream/electron-shm-viewer/validation.md)
- [references/exact-brep-in-usd/README.md](upstream/exact-brep-in-usd/README.md)
- [references/gl-viewport-overlay/README.md](upstream/gl-viewport-overlay/README.md)
- [references/gl-viewport-overlay/architecture.md](upstream/gl-viewport-overlay/architecture.md)
- [references/gl-viewport-overlay/example-gizmo.md](upstream/gl-viewport-overlay/example-gizmo.md)
- [references/gl-viewport-overlay/interaction-pattern.md](upstream/gl-viewport-overlay/interaction-pattern.md)
- [references/gl-viewport-overlay/projection-alignment.md](upstream/gl-viewport-overlay/projection-alignment.md)
- [references/headless-shm-cli/README.md](upstream/headless-shm-cli/README.md)
- [references/huggingface-usd/README.md](upstream/huggingface-usd/README.md)
- [references/interaction-round-trip/README.md](upstream/interaction-round-trip/README.md)
- [references/local-viewer/README.md](upstream/local-viewer/README.md)
- [references/native-picking-selection/README.md](upstream/native-picking-selection/README.md)
- [references/navigation-presets/README.md](upstream/navigation-presets/README.md)
- [references/navigation-presets/preset-camera-ops.md](upstream/navigation-presets/preset-camera-ops.md)
- [references/newton-physics/README.md](upstream/newton-physics/README.md)
- [references/object-selection/README.md](upstream/object-selection/README.md)
- [references/ovrtx-rendering/README.md](upstream/ovrtx-rendering/README.md)
- [references/ovstage-data-plane/README.md](upstream/ovstage-data-plane/README.md)
- [references/ovstage-live-geometry/README.md](upstream/ovstage-live-geometry/README.md)
- [references/ovstage-ovrtx-integration/README.md](upstream/ovstage-ovrtx-integration/README.md)
- [references/ovstage-population/README.md](upstream/ovstage-population/README.md)
- [references/ovstage-runtime/README.md](upstream/ovstage-runtime/README.md)
- [references/ovui-library/README.md](upstream/ovui-library/README.md)
- [references/ovui-library/api-reference.md](upstream/ovui-library/api-reference.md)
- [references/ovui-library/extending.md](upstream/ovui-library/extending.md)
- [references/ovui-local-viewer-recipe/README.md](upstream/ovui-local-viewer-recipe/README.md)
- [references/ovui-local-viewer-recipe/interaction-features.md](upstream/ovui-local-viewer-recipe/interaction-features.md)
- [references/ovui-local-viewer-recipe/project-structure.md](upstream/ovui-local-viewer-recipe/project-structure.md)
- [references/ovui-local-viewer-recipe/setup-shell-renderer.md](upstream/ovui-local-viewer-recipe/setup-shell-renderer.md)
- [references/ovui-local-viewer-recipe/validation-build-order.md](upstream/ovui-local-viewer-recipe/validation-build-order.md)
- [references/ovwidgets-editor-shell/README.md](upstream/ovwidgets-editor-shell/README.md)
- [references/ovxr-composition-ui-validation/README.md](upstream/ovxr-composition-ui-validation/README.md)
- [references/ovxr-composition-ui-validation/evidence-gates.md](upstream/ovxr-composition-ui-validation/evidence-gates.md)
- [references/ovxr-composition-ui-validation/frustum-placement.md](upstream/ovxr-composition-ui-validation/frustum-placement.md)
- [references/ovxr-composition-ui-validation/library-only-validation.md](upstream/ovxr-composition-ui-validation/library-only-validation.md)
- [references/ovxr-composition-ui-validation/owned-orchestration.md](upstream/ovxr-composition-ui-validation/owned-orchestration.md)
- [references/ovxr-composition-ui-validation/viewer-evidence.md](upstream/ovxr-composition-ui-validation/viewer-evidence.md)
- [references/ovxr-composition-ui/README.md](upstream/ovxr-composition-ui/README.md)
- [references/ovxr-composition-ui/async-raster-pipeline.md](upstream/ovxr-composition-ui/async-raster-pipeline.md)
- [references/ovxr-composition-ui/compositor-passes-and-sync.md](upstream/ovxr-composition-ui/compositor-passes-and-sync.md)
- [references/ovxr-composition-ui/depth-tools.md](upstream/ovxr-composition-ui/depth-tools.md)
- [references/ovxr-composition-ui/editor-document-model.md](upstream/ovxr-composition-ui/editor-document-model.md)
- [references/ovxr-composition-ui/experience-quality.md](upstream/ovxr-composition-ui/experience-quality.md)
- [references/ovxr-composition-ui/foveation-and-edge-math.md](upstream/ovxr-composition-ui/foveation-and-edge-math.md)
- [references/ovxr-composition-ui/library-only-compositor.md](upstream/ovxr-composition-ui/library-only-compositor.md)
- [references/ovxr-composition-ui/native-build-and-discovery.md](upstream/ovxr-composition-ui/native-build-and-discovery.md)
- [references/ovxr-composition-ui/performance-and-telemetry.md](upstream/ovxr-composition-ui/performance-and-telemetry.md)
- [references/ovxr-composition-ui/primary-projection-compositor.md](upstream/ovxr-composition-ui/primary-projection-compositor.md)
- [references/ovxr-composition-ui/primary-projection.md](upstream/ovxr-composition-ui/primary-projection.md)
- [references/ovxr-composition-ui/projection-and-depth.md](upstream/ovxr-composition-ui/projection-and-depth.md)
- [references/ovxr-composition-ui/raster-abi.md](upstream/ovxr-composition-ui/raster-abi.md)
- [references/ovxr-composition-ui/sdk-frame-backend.md](upstream/ovxr-composition-ui/sdk-frame-backend.md)
- [references/ovxr-composition-ui/skia-yoga.md](upstream/ovxr-composition-ui/skia-yoga.md)
- [references/ovxr-composition-ui/spatial-interaction.md](upstream/ovxr-composition-ui/spatial-interaction.md)
- [references/ovxr-composition-ui/spatial-surfaces-and-interaction.md](upstream/ovxr-composition-ui/spatial-surfaces-and-interaction.md)
- [references/ovxr-composition-ui/telemetry-contract.md](upstream/ovxr-composition-ui/telemetry-contract.md)
- [references/ovxr-composition-ui/validation-and-live-gates.md](upstream/ovxr-composition-ui/validation-and-live-gates.md)
- [references/ovxr-foveation-and-display/README.md](upstream/ovxr-foveation-and-display/README.md)
- [references/ovxr-frame-loop-and-readback/README.md](upstream/ovxr-frame-loop-and-readback/README.md)
- [references/ovxr-library-runtime/README.md](upstream/ovxr-library-runtime/README.md)
- [references/ovxr-library-runtime/ar-compositing.md](upstream/ovxr-library-runtime/ar-compositing.md)
- [references/ovxr-library-runtime/frame-input-order.md](upstream/ovxr-library-runtime/frame-input-order.md)
- [references/ovxr-library-runtime/library-only.md](upstream/ovxr-library-runtime/library-only.md)
- [references/ovxr-library-runtime/live-ar-controls.md](upstream/ovxr-library-runtime/live-ar-controls.md)
- [references/ovxr-library-runtime/mirror-lifetime.md](upstream/ovxr-library-runtime/mirror-lifetime.md)
- [references/ovxr-library-runtime/settings-and-lifetime.md](upstream/ovxr-library-runtime/settings-and-lifetime.md)
- [references/ovxr-library-runtime/viewer-assembly.md](upstream/ovxr-library-runtime/viewer-assembly.md)
- [references/ovxr-openxr-runtime/README.md](upstream/ovxr-openxr-runtime/README.md)
- [references/ovxr-python-interactions/README.md](upstream/ovxr-python-interactions/README.md)
- [references/ovxr-python-interactions/architecture.md](upstream/ovxr-python-interactions/architecture.md)
- [references/ovxr-python-interactions/feature-patterns.md](upstream/ovxr-python-interactions/feature-patterns.md)
- [references/physics-simulation/README.md](upstream/physics-simulation/README.md)
- [references/prim-info-display/README.md](upstream/prim-info-display/README.md)
- [references/prim-pick-effects/README.md](upstream/prim-pick-effects/README.md)
- [references/prim-transform-safety/README.md](upstream/prim-transform-safety/README.md)
- [references/realtime-sim-integration/README.md](upstream/realtime-sim-integration/README.md)
- [references/render-settings/README.md](upstream/render-settings/README.md)
- [references/routing.md](upstream/routing.md)
- [references/section-views/README.md](upstream/section-views/README.md)
- [references/seg-outline-highlight/README.md](upstream/seg-outline-highlight/README.md)
- [references/selection-animation/README.md](upstream/selection-animation/README.md)
- [references/selection-feedback/README.md](upstream/selection-feedback/README.md)
- [references/smlib-brep-pitfalls/README.md](upstream/smlib-brep-pitfalls/README.md)
- [references/spg-processing/README.md](upstream/spg-processing/README.md)
- [references/stage-attribute-reads/README.md](upstream/stage-attribute-reads/README.md)
- [references/stage-hierarchy/README.md](upstream/stage-hierarchy/README.md)
- [references/stage-hierarchy/fallback-worker-protocol.md](upstream/stage-hierarchy/fallback-worker-protocol.md)
- [references/stage-loading/README.md](upstream/stage-loading/README.md)
- [references/stage-management/README.md](upstream/stage-management/README.md)
- [references/stage-queries/README.md](upstream/stage-queries/README.md)
- [references/streaming-client/README.md](upstream/streaming-client/README.md)
- [references/streaming-lifecycle/README.md](upstream/streaming-lifecycle/README.md)
- [references/streaming-messages/README.md](upstream/streaming-messages/README.md)
- [references/streaming-messages/server-handler-map.md](upstream/streaming-messages/server-handler-map.md)
- [references/streaming-server/README.md](upstream/streaming-server/README.md)
- [references/streaming-server/frame-loop-and-continuity.md](upstream/streaming-server/frame-loop-and-continuity.md)
- [references/streaming-viewer-recipe/README.md](upstream/streaming-viewer-recipe/README.md)
- [references/streaming-viewer-recipe/client-protocol.md](upstream/streaming-viewer-recipe/client-protocol.md)
- [references/streaming-viewer-recipe/interaction-features.md](upstream/streaming-viewer-recipe/interaction-features.md)
- [references/streaming-viewer-recipe/project-structure.md](upstream/streaming-viewer-recipe/project-structure.md)
- [references/streaming-viewer-recipe/server-runtime.md](upstream/streaming-viewer-recipe/server-runtime.md)
- [references/streaming-viewer-recipe/validation-build-order.md](upstream/streaming-viewer-recipe/validation-build-order.md)
- [references/streaming-vs-local/README.md](upstream/streaming-vs-local/README.md)
- [references/stylized-visualization/README.md](upstream/stylized-visualization/README.md)
- [references/stylized-visualization/aov-guide-contracts.md](upstream/stylized-visualization/aov-guide-contracts.md)
- [references/stylized-visualization/implementation.md](upstream/stylized-visualization/implementation.md)
- [references/stylized-visualization/line-compositor-delivery.md](upstream/stylized-visualization/line-compositor-delivery.md)
- [references/stylized-visualization/mesh-xray.md](upstream/stylized-visualization/mesh-xray.md)
- [references/stylized-visualization/reproduction-validation.md](upstream/stylized-visualization/reproduction-validation.md)
- [references/stylized-visualization/style-composition-contract.md](upstream/stylized-visualization/style-composition-contract.md)
- [references/stylized-visualization/style-recipes.md](upstream/stylized-visualization/style-recipes.md)
- [references/stylized-visualization/usd-brep-source.md](upstream/stylized-visualization/usd-brep-source.md)
- [references/subprocess-geometry-bridge/README.md](upstream/subprocess-geometry-bridge/README.md)
- [references/tauri-local-viewer/README.md](upstream/tauri-local-viewer/README.md)
- [references/tauri-shm-transform-gizmo/README.md](upstream/tauri-shm-transform-gizmo/README.md)
- [references/transform-manipulator/README.md](upstream/transform-manipulator/README.md)
- [references/troubleshooting/README.md](upstream/troubleshooting/README.md)
- [references/troubleshooting/scenario-playbooks.md](upstream/troubleshooting/scenario-playbooks.md)
- [references/usd-sample-data/README.md](upstream/usd-sample-data/README.md)
- [references/usd-viewer-app/README.md](upstream/usd-viewer-app/README.md)
- [references/validation.md](upstream/validation.md)
- [references/viewer-backend-interface/README.md](upstream/viewer-backend-interface/README.md)
- [references/viewer-control-patterns/README.md](upstream/viewer-control-patterns/README.md)
- [references/viewer-data-view-patterns/README.md](upstream/viewer-data-view-patterns/README.md)
- [references/viewer-feedback-status/README.md](upstream/viewer-feedback-status/README.md)
- [references/viewer-input-routing/README.md](upstream/viewer-input-routing/README.md)
- [references/viewer-layout-patterns/README.md](upstream/viewer-layout-patterns/README.md)
- [references/viewer-ux-workflow/README.md](upstream/viewer-ux-workflow/README.md)
- [references/viewport-overlays/README.md](upstream/viewport-overlays/README.md)
- [references/viewport-overlays/cuda-compositing.md](upstream/viewport-overlays/cuda-compositing.md)
- [references/viewport-resize/README.md](upstream/viewport-resize/README.md)
- [references/vulkan-compositing/README.md](upstream/vulkan-compositing/README.md)
- [references/vulkan-compositing/depth-overlays.md](upstream/vulkan-compositing/depth-overlays.md)
- [references/vulkan-compositing/interop-and-lifecycle.md](upstream/vulkan-compositing/interop-and-lifecycle.md)
- [references/webgl-shm-transport/README.md](upstream/webgl-shm-transport/README.md)
- [references/windows-native-setup/README.md](upstream/windows-native-setup/README.md)
- [references/xr-client-connection/README.md](upstream/xr-client-connection/README.md)
- [references/xr-client-message-contract/README.md](upstream/xr-client-message-contract/README.md)
- [references/xr-desktop-mirror/README.md](upstream/xr-desktop-mirror/README.md)
- [references/xr-session-modes-and-passthrough/README.md](upstream/xr-session-modes-and-passthrough/README.md)
- [references/xr-spatial-input/README.md](upstream/xr-spatial-input/README.md)
- [references/xr-spatial-input/advanced-tools.md](upstream/xr-spatial-input/advanced-tools.md)
- [references/xr-spatial-input/controllers.md](upstream/xr-spatial-input/controllers.md)
- [references/xr-spatial-input/feature-validation.md](upstream/xr-spatial-input/feature-validation.md)
- [references/xr-spatial-input/gesture-arbitration.md](upstream/xr-spatial-input/gesture-arbitration.md)
- [references/xr-spatial-input/gesture-filtering.md](upstream/xr-spatial-input/gesture-filtering.md)
- [references/xr-spatial-input/hand-recognizers.md](upstream/xr-spatial-input/hand-recognizers.md)
- [references/xr-spatial-input/hands.md](upstream/xr-spatial-input/hands.md)
- [references/xr-spatial-input/navigation.md](upstream/xr-spatial-input/navigation.md)
- [references/xr-spatial-input/physics-interaction.md](upstream/xr-spatial-input/physics-interaction.md)
- [references/xr-spatial-input/simulation-lifecycle.md](upstream/xr-spatial-input/simulation-lifecycle.md)
- [references/xr-spatial-input/stage-composition.md](upstream/xr-spatial-input/stage-composition.md)
- [references/xr-spatial-input/teleport-acceptance.md](upstream/xr-spatial-input/teleport-acceptance.md)
- [references/xr-spatial-input/webxr-client.md](upstream/xr-spatial-input/webxr-client.md)
- [references/xr-tracking-anchor-and-scale/README.md](upstream/xr-tracking-anchor-and-scale/README.md)
- [references/xr-viewer-recipe/README.md](upstream/xr-viewer-recipe/README.md)
