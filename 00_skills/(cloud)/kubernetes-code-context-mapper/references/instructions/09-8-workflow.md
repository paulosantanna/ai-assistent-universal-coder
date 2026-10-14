<!-- Package: 00_skills/(cloud)/kubernetes-code-context-mapper; relative command/resource examples resolve from that package or workspace root. -->

## 8. Workflow

1. Validate scope, read-only boundary, namespace and object identifiers.
2. Collect available local manifests before relying on cluster exports.
3. Resolve object hierarchy:
   - pod;
   - ReplicaSet, Job, StatefulSet, DaemonSet or controller;
   - deployment or higher-level release;
   - service, ingress or route;
   - image and build metadata.
4. Resolve selectors and labels without assuming uniqueness.
5. Map image tags, annotations or GitOps metadata to commit, package or module.
6. Map telemetry identifiers:
   - `service.name`;
   - namespace;
   - pod;
   - container;
   - node;
   - workload;
   - deployment environment.
7. Search repository paths for manifests, service names, ports, health probes, metrics names and trace attributes.
8. Identify ownership, tests, rollback and remediation boundaries.
9. Surface contradictions and missing metadata.
10. Produce evidence-backed mapping and downstream handoff if needed.
11. Apply the honest evaluator before completion.
