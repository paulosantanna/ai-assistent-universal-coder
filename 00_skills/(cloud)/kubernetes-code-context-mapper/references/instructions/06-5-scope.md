<!-- Package: 00_skills/(cloud)/kubernetes-code-context-mapper; relative command/resource examples resolve from that package or workspace root. -->

## 5. Scope

### Included

- Map pod to owner workload by metadata, owner references, labels and selectors.
- Map workload to image, build tag, commit SHA, deployment manifest, Helm/Kustomize chart or CI artifact when available.
- Map service and ingress routes to application entrypoints.
- Map logs, metrics and traces to code ownership using OpenTelemetry resource attributes and Kubernetes metadata.
- Identify tests that should cover the affected module.
- Produce downstream handoff boundaries for repair, architecture or observability work.

### Excluded

- Applying Kubernetes manifests.
- Scaling, restarting or deleting workloads.
- Fetching secrets or unredacted config values.
- Claiming ownership from labels alone when selectors, manifests or build metadata contradict it.
