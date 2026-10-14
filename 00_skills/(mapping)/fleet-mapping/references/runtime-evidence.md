# Repository snapshot and production runtime

Updated: 2026-10-13
Entry point: ../SKILL.md. Source: IMG_2736–IMG_2737.

A default branch is static source evidence, not the image the production Route currently selects. Blue/green labels are clues; prove the actual Route → Service → workload → image/tag/digest and environment using authorized read-only tools. “Green is live” is a photographed convention, not a universal invariant.
Production may have two regions/clusters and slots running different versions. Homologation may have one cluster. Compare every actually inventoried region for the requested environment, without assuming South/North host names from the photo. Timestamp runtime evidence, separate it from canonical source notes and record unavailable regions explicitly.
For front-end MFEs, the shell/release wrapper image alone may not identify the embedded library versions; inspect wrapper release metadata and authorized artifact manifests. Production/homologation facts must be attributed to their environment.
The photo names openshift-recon, but this workspace has no verified binding for it. Use available read-only openshift-observability-staff/kubernetes-code-context-mapper capabilities after prerequisite verification. Missing access blocks runtime claims, not static mapping.
